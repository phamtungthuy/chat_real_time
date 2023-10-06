from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse, inline_serializer
from drf_spectacular.types import OpenApiTypes
from .serializer import UserSerializer, FriendSerializer
from django.contrib.auth.models import User
from user.models import UserProfile, Friend
from channel.serializer import ChannelSerializer
from .response import ResponseSerializer, SuccessResponseSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from storages.backends.s3boto3 import S3Boto3Storage
from django.db.models import Q
import uuid
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

from django.core import mail
import random
from django.template.loader import render_to_string
from django.utils.html import strip_tags

@extend_schema(tags=['User'])
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
   
    def get_permissions(self):
        # Allow all actions except retrieve
        if self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


    @extend_schema(
        responses={
            200: OpenApiResponse(response=SuccessResponseSerializer,
                                 description="Operations successfully"),
            404: OpenApiResponse(response=ResponseSerializer,
                                 description="User not found!")
        }
        # more customizations
    )


    def retrieve(self, request, id=None, username=None):
        try:
            if id is None:
                user = User.objects.get(username=username)
            else:
                user = User.objects.get(id=id)
            serializer = UserSerializer(user)
        except User.DoesNotExist:
            return Response({'message': f'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message': 'Successfully',
                         'data': serializer.get()}, status=status.HTTP_200_OK)
    
    @extend_schema(
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "username": {"type": "string", "required": True},
                    "password": {"type": "string"},
                    "email": {"type": "string"}},
            },
        },
        responses = {
            200: OpenApiResponse(response=SuccessResponseSerializer, description='Operations successfully'),
            400: OpenApiResponse(response=ResponseSerializer, description='Bad Request')
        }
    )
    
    def create(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            # Generate four number verification code
            verification_code = str(random.randint(0, 9999))
            while len(verification_code) < 4:
                verification_code = "0" + verification_code
            # Create user profile ref to User
            userProfile = UserProfile.objects.create(user=user, verification_code=verification_code)
            # Send verification code via user email
            html_message = render_to_string('email_form.html', {'verification_code': verification_code})
            plain_message = f"Mã xác thực của bạn: {verification_code}"
            mail.send_mail(
                subject="Verification code",
                from_email='Schat <schatemail.system@gmail.com>',
                message=plain_message,
                recipient_list=[user.email],
                html_message=html_message
            )
            return Response({"message": "Verification code was sent", "data": serializer.get()})
            # return Response({
            #     'message': 'Account created successfully',
            #     'data': serializer.get()
            #     },status=status.HTTP_200_OK)
        message = ""
        for key, value in serializer.errors.items():
            message += value[0]
            break
        return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)
    

    def verifyEmail(self, request):
        userId = request.data.get('userId')
        verification_code = request.data.get('verification_code')
        try:
            user = User.objects.get(pk=userId)
            userProfile = UserProfile.objects.get(user=user)
        except User.DoesNotExist:
            return Response({'message': 'User not found'},status=status.HTTP_404_NOT_FOUND)
        if userProfile.verification_code == verification_code:
            userProfile.verified = True
            userProfile.save()
            return Response({"message": "Account has been verified successfully"})
        else: 
            return Response({"message": "Verification code not correct"})


    @extend_schema(
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "password": {"type": "string"},
                    "email": {"type": "string"}},
            },
        },
        responses={
            200: OpenApiResponse(response=SuccessResponseSerializer,
                                 description="Operations successfully"),
            404: OpenApiResponse(response=ResponseSerializer,
                                 description="User not found!")
        }
        # more customizations
    )
    def update(self, request, id=None, username=None):
        try:
            if id is None:
                user = User.objects.get(username=username)
            else:
                user = User.objects.get(id=id)
            data = request.data
            serializer = UserSerializer(instance=user, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Updated successfuly'}, status=status.HTTP_200_OK)
            message = ""
            for key, value in serializer.errors.items():
                message += value[0]
                break
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'message': f'User not found'},status=status.HTTP_404_NOT_FOUND)
        return Response({'message': 'Error when updating'}, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        responses={
            200: OpenApiResponse(response=SuccessResponseSerializer,
                                 description="Operations successfully"),
            404: OpenApiResponse(response=ResponseSerializer,
                                 description="User not found!")
        }
        # more customizations
    )
    def delete(self, request, id=None, username=None):
        try:
            if id is None:
                user = User.objects.get(username=username)
            else:
                user = User.objects.get(id=id)
            user.delete()
        except User.DoesNotExist:
            return Response({'message': f'User not found'},status=status.HTTP_404_NOT_FOUND)
        return Response({'message': 'Deleted user successfully!'}, status=status.HTTP_200_OK)
    
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
            data = {
                "avatar_url": file_url
            }
            return Response({"message": "Update user avatar successfully", "data": data})
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def getChannelList(self, request):
        user = request.user
        members = user.members.all()
        channels = [member.channel for member in members]
        serializer = ChannelSerializer(channels, many=True)
        return Response({'message': 'Get channel list successfully', 'data': serializer.data})

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