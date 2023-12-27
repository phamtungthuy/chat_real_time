from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse, inline_serializer
from drf_spectacular.types import OpenApiTypes
from .serializer import UserSerializer, FriendSerializer, UserProfileSerializer, NotificationSerializer
from django.contrib.auth.models import User
from user.models import UserProfile, Friend, Notification
from channel.serializer import ChannelSerializer
from .schema import *
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from storages.backends.s3boto3 import S3Boto3Storage
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
import uuid, json, base64
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .utils import sendVerificationEmail, resendVerificationEmail

@extend_schema(tags=['User'])
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
   
    def get_permissions(self):
        admin_actions = ['getAllUsers', 'banUser']
        authenticate_actions = ['retrieveUser', 'getChannelList']
        if self.action in authenticate_actions:
            permission_classes = [IsAuthenticated]
        elif self.action in admin_actions:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


    @getAllUsersSchema
    def getAllUsers(self, request):
        users = self.queryset
        serializer = self.serializer_class(users, many=True)
        return Response({"message": "Get all users successfully", "data": serializer.data})


    @retrieveUserSchema
    def retrieveUser(self, request):
        try:
            user = request.user
            serializer = self.serializer_class(user, many=False)
            return Response({'message': 'Get user successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    

    @signUpSchema
    def signup(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            sendVerificationEmail(user, user.email)
            return Response({"message": "Verification code was sent", "data": serializer.data})
        except serializers.ValidationError as e:
            message = ""
            for key, value in serializer.errors.items():
                message += f'{value[0]} ({key})'
                break
            if not message: message = e.args[0]
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)
    
    @resendVerificationSchema
    def resendVerification(self, request):
        data = request.data
        username = data.get('username')
        email = data.get('email')
        try:
            user = User.objects.get(username=username)
            if not resendVerificationEmail(user, email):
                return Response({'message': 'User has been already verified'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "Verification code was resent", 'data': data})
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
    @verifyEmailSchema
    def verifyEmail(self, request):
        data = request.data
        verification_code = data.get('verification_code')
        email_base64 = verification_code[:-6]
        email_bytes = base64.b64decode(email_base64.encode("ascii"))
        email = email_bytes.decode("ascii")
        users = User.objects.filter(email=email)
        if not users:
            return Response({'message': 'User not found'},status=status.HTTP_404_NOT_FOUND)
        for user in users:
            userProfile = UserProfile.objects.get(user=user)
            if userProfile.verified:
                return Response({'message': 'User has been already verified'}, status=status.HTTP_400_BAD_REQUEST)
            elif (userProfile.verification_code == verification_code and userProfile.verification_code is not None):
                userProfile.verified = True
                userProfile.verification_code = None
                userProfile.save()
                return Response({"message": "User has been verified successfully"})
        return Response({"message": "Verification code not correct"}, status=status.HTTP_400_BAD_REQUEST)


    @loginSchema
    def login(self, request):
        username = request.data.get('username', None)
        email = request.data.get('email', None)
        password = request.data.get('password')
        try:
            if username is not None:
                user = User.objects.get(username=username)
            else:
                user = User.objects.get(email=email)
            if (user.check_password(password)):
                userProfile = UserProfile.objects.get(user=user)
                if user.is_active:
                    if (userProfile.verified):
                        refresh = RefreshToken.for_user(user)
                        token = {
                            'refresh': str(refresh),
                            'access': str(refresh.access_token)
                        }
                        return Response({"message": "Login successfully", "data": token})
                    else:
                        return Response({"message": "User has not been verified"}, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    return Response({"message": "User has been banned"}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({'message': "Password not match"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"message": "Username or email not match"}, status=status.HTTP_404_NOT_FOUND)

    @changePasswordSchema
    def changePassword(self, request):
        user = request.user
        oldPassword = request.data.get('oldPassword', None)
        newPassword = request.data.get('newPassword', None)
        if oldPassword is None or newPassword is None:
            return Response({'message': 'Both old password and new password must be provided'}, status=status.HTTP_400_BAD_REQUEST)
        if (user.check_password(oldPassword)):
            serializer = self.serializer_class(instance=user, data={'password': newPassword}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Update password successfuly'}, status=status.HTTP_200_OK)
            message = ""
            for key, value in serializer.errors.items():
                message += f'{value[0]} ({key})'
                break
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Password not match'}, status=status.HTTP_400_BAD_REQUEST)
            
    @changeEmailSchema
    def changeEmail(self, request):
        user = request.user
        newEmail = request.data.get('newEmail', None)
        if newEmail is None:
            return Response({'message': 'New email must be provided if you want to change email'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(instance=user, data={'email': newEmail}, partial=True)
        if serializer.is_valid():
            sendVerificationEmail(user, newEmail)
            return Response({'message': 'Verification code was sent to your new email'}, status=status.HTTP_200_OK)
        message = ""
        for key, value in serializer.errors.items():
            message += f'{value[0]} ({key})'
            break
        return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

    @verifyChangeEmailSchema
    def verifyChangeEmail(self, request):
        user = request.user
        userProfile = user.profile
        verification_code = request.data.get('verification_code', None)
        if (verification_code == userProfile.verification_code and userProfile.verification_code is not None):
            newEmail_base64 = verification_code[:-6]
            newEmail_bytes = base64.b64decode(newEmail_base64.encode("ascii"))
            newEmail = newEmail_bytes.decode("ascii")
            user.email = newEmail
            user.save()
            userProfile.verification_code = None
            userProfile.save()
            return Response({'message': 'Change email successfuly'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Verification code not correct'}, status=status.HTTP_400_BAD_REQUEST)

    @banUserSchema
    def banUser(self, request, userId):
        try:
            user = User.objects.get(pk=userId)
            text_data_json = {
                "action": "ban_user",
                "target": "user",
                "targetId": user.id,
                "data": {
                    "message": "Your account has been banned by admin"
                }
            }
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(f'user_{user.id}', {
                "type": "chat.send",
                "text_data_json": text_data_json
            })
            user.is_active = False
            user.save()
            return Response({'message': 'Banned user successfully'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @getChannelListSchema
    def getChannelList(self, request):
        user = request.user
        members = user.members.all()
        channels = [member.channel for member in members]
        serializer = ChannelSerializer(channels, many=True)
        return Response({'message': 'Get channel list successfully', 'data': serializer.data})

@extend_schema(tags=['User Profile'])
class UserProfileViewSet(viewsets.ViewSet):
    query_set = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    @getUserProfileSchema
    def getUserProfile(self, request, userId):
        try:
            user = request.user
            userProfile = self.query_set.get(user_id=userId)
            serializer = self.serializer_class(userProfile, many=False)
            isSelf = (user.id == userId)
            # If user get self profile, return full info
            if isSelf:
                return Response({"message": "Get user profile successfully", "data": serializer.data})
            # If user get friend profile, return friend info
            isFriend = Friend.objects.filter(Q(user=user, friend_with=userId) | Q(user_id=userId, friend_with=user)).exists()
            if isFriend:
                return Response({"message": "Get user profile successfully", "data": serializer.getFriendProfile()})
            else: # If not friend return public info
                return Response({"message": "Get user profile successfully", "data": serializer.getStrangerProfile()})
        except UserProfile.DoesNotExist:
            return Response({"message": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)

    @getSelfProfileSchema
    def getSelfProfile(self, request):
        try:
            user = request.user
            userProfile = self.query_set.get(user=user)
            serializer = self.serializer_class(userProfile, many=False)
            return Response({"message": "Get self profile successfully", "data": serializer.data})
        except UserProfile.DoesNotExist:
            return Response({"message": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)

    @updateUserProfileSchema
    def updateUserProfile(self, request):
        user = request.user
        data = request.data
        userProfile = self.query_set.get(user=user)
        profileSerializer = self.serializer_class(instance=userProfile, data=data, partial=True)
        userSerializer = UserSerializer(instance=user, data=data, partial=True)
        if userSerializer.is_valid() and profileSerializer.is_valid():
            userSerializer.save()
            profileSerializer.save()
            return Response({'message': 'Update user profile successfuly', "data": profileSerializer.data})
        message = ""
        if userSerializer.errors:
            errors = userSerializer.errors
        else:
            errors = profileSerializer.errors
        for key, value in errors.items():
            message += f'{value[0]} ({key})'
            break
        return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

    @uploadUserAvatarSchema
    def uploadUserAvatar(self, request):
        file_obj = request.FILES.get('file')
        print(request.FILES)
        # Validate file
        if file_obj is None:
            return Response({"message": "File not provided"}, status=status.HTTP_400_BAD_REQUEST) 
        file_type = file_obj.content_type.split('/')[0]
        if file_type != 'image':
            return Response({"message": "File type not supported"}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        elif file_obj.size > 10**7:
            return Response({"message": "File size is too large"}, status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)
        # Upload file to s3
        user = request.user
        userProfile = UserProfile.objects.get(user=user)
        file_path = f'upload/user/{user.id}_{user.username}/avatar/{uuid.uuid4()}'
        s3 = S3Boto3Storage()
        s3.save(file_path, file_obj)
        file_url = s3.url(file_path)
        # Save to db as message
        try:
            userProfile.avatar_url = file_url
            userProfile.save()
            return Response({"message": "Update user avatar successfully", "data": {"avatar_url": file_url}})
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Friend'])
class FriendViewSet(viewsets.ViewSet):
    query_set = Friend.objects.all()
    serializer_class = FriendSerializer
    permission_classes = [IsAuthenticated]

    @getFriendListSchema
    def getFriendList(self, request):
        user = request.user
        friendList = user.friends.all()
        serializer = self.serializer_class(friendList, many=True)
        return Response({'message': 'Get friend list successfully', 'data': serializer.data})

    @deleteFriendSchema
    def deleteFriend(self, request, friendId):
        user = request.user
        try:
            friend = Friend.objects.filter(Q(user=user, friend_with=friendId) | Q(user_id=friendId, friend_with=user))
            friend.delete()
            return Response({'message': 'Delete friend successfully'})
        except Friend.DoesNotExist:
            return Response({"message": "Friend not found"}, status=status.HTTP_404_NOT_FOUND)

@extend_schema(tags=['Notification'])
class NotificationViewSet(viewsets.ViewSet):
    query_set = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    @getNotificationListSchema
    def getNotificationList(self, request):
        user = request.user
        notificationList = user.notifications.all()
        serializer = self.serializer_class(notificationList, many=True)
        return Response({'message': 'Get notification list successfully', 'data': serializer.data})

    @getSentFriendRequestListSchema
    def getSentFriendRequestList(self, request):
        user = request.user
        sentFriendRequestList = Notification.objects.filter(sender=user, notification_type='friend_request')
        serializer = self.serializer_class(sentFriendRequestList, many=True)
        return Response({'message': 'Get sent friend request list successfully', 'data': serializer.data})


    
