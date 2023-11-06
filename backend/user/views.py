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
import uuid
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from .utils import sendVerificationEmail, resendVerificationEmail


@extend_schema(tags=['User'])
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
   
    def get_permissions(self):
        admin_actions = ['getAllUsers', 'banUser']
        authenticate_actions = ['retrieve', 'getChannelList']
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


    # @extend_schema(
    #     responses={
    #         200: OpenApiResponse(response=SuccessResponseSerializer,
    #                              description="Operations successfully"),
    #         404: OpenApiResponse(response=ResponseSerializer,
    #                              description="User not found!")
    #     }
    #     # more customizations
    # )
    # def retrieve(self, request, id=None, username=None):
    #     try:
    #         if id is None:
    #             user = User.objects.get(username=username)
    #         else:
    #             user = User.objects.get(id=id)
    #         serializer = UserSerializer(user)
    #     except User.DoesNotExist:
    #         return Response({'message': f'User not found'}, status=status.HTTP_404_NOT_FOUND)
    #     return Response({'message': 'Successfully',
    #                      'data': serializer.data}, status=status.HTTP_200_OK)
    @signUpSchema
    def signup(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            sendVerificationEmail(user)
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
        username = data.get('username')
        verification_code = data.get('verification_code')
        try:
            user = User.objects.get(username=username)
            userProfile = UserProfile.objects.get(user=user)
            if userProfile.verified:
                return Response({'message': 'User has been already verified'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'message': 'User not found'},status=status.HTTP_404_NOT_FOUND)
        # Verify
        if userProfile.verification_code == verification_code:
            userProfile.verified = True
            userProfile.save()
            return Response({"message": "User has been verified successfully"})
        else: 
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
                return Response({'message': "Password not match"})
        except User.DoesNotExist:
            return Response({"message": "Username or email not match"}, status=status.HTTP_404_NOT_FOUND)



    # @extend_schema(
    #     request={
    #         "multipart/form-data": {
    #             "type": "object",
    #             "properties": {
    #                 "password": {"type": "string"},
    #                 "email": {"type": "string"}},
    #         },
    #     },
    #     responses={
    #         200: OpenApiResponse(response=SuccessResponseSerializer,
    #                              description="Operations successfully"),
    #         404: OpenApiResponse(response=ResponseSerializer,
    #                              description="User not found!")
    #     }
    #     # more customizations
    # )
    # def update(self, request, id=None, username=None):
    #     try:
    #         if id is None:
    #             user = User.objects.get(username=username)
    #         else:
    #             user = User.objects.get(id=id)
    #         data = request.data
    #         serializer = UserSerializer(instance=user, data=data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response({'message': 'Updated successfuly'}, status=status.HTTP_200_OK)
    #         message = ""
    #         for key, value in serializer.errors.items():
    #             message += f'{value[0]} ({key})'
    #             break
    #         return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)
    #     except User.DoesNotExist:
    #         return Response({'message': f'User not found'},status=status.HTTP_404_NOT_FOUND)
    #     return Response({'message': 'Error when updating'}, status=status.HTTP_400_BAD_REQUEST)
    

    # @extend_schema(
    #     responses={
    #         200: OpenApiResponse(response=SuccessResponseSerializer,
    #                              description="Operations successfully"),
    #         404: OpenApiResponse(response=ResponseSerializer,
    #                              description="User not found!")
    #     }
    # )
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


    def updateUserProfile(self, request):
        user = request.user
        data = request.data
        userProfile = self.query_set.get(user=user)
        serializer = UserProfileSerializer(instance=userProfile, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Update user profile successfuly', "data": serializer.data})
        message = ""
        for key, value in serializer.errors.items():
            message += f'{value[0]} ({key})'
            break
        return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)


    def uploadUserAvatar(self, request):
        file_obj = request.FILES.get('file')
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

    def getFriendList(self, request):
        user = request.user
        friendList = user.friends.all()
        serializer = self.serializer_class(friendList, many=True)
        return Response({'message': 'Get friend list successfully', 'data': serializer.data})

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

    def getNotificationList(self, request):
        user = request.user
        notificationList = user.notifications.all()
        serializer = self.serializer_class(notificationList, many=True)
        return Response({'message': 'Get notification list successfully', 'data': serializer.data})


    