from rest_framework import serializers
from drf_spectacular.utils import inline_serializer
from .serializer import *
from channel.serializer import ChannelSerializer
from django import forms

class ResendVerificationSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()

class UserLoginSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
class UserResponseSerializer(UserSerializer):
    fullname = serializers.CharField()
    class Meta:
        model = User
        fields = ['id', 'username', 'avatar_url', 'email', 
                  'first_name', 'last_name', 'fullname']
        
class UserWithoutEmailSerializer(UserResponseSerializer):
    fullname = serializers.CharField()
    class Meta:
        model = User
        fields = ['id', 'username', 'avatar_url', 
                  'first_name', 'last_name', 'fullname']
        
        
class GeneralMessageSerializer(serializers.Serializer):
    message = serializers.CharField()
    
class SuccessSignUpSerializer(serializers.Serializer):
    message = serializers.CharField()
    data = UserResponseSerializer()
    
class verifyEmailSerializer(serializers.Serializer):
    username = serializers.CharField()
    verification_code = serializers.CharField(max_length=10)
    
class TokenDataSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
    
class SuccessUserLoginSerializer(serializers.Serializer):
    message = serializers.CharField()
    data = TokenDataSerializer()
    
class SuccessResendVerificationCode(serializers.Serializer):
    message =serializers.CharField()
    data = ResendVerificationSerializer()

class SuccessGetAllUsersSerializer(serializers.Serializer):
    message =serializers.CharField()
    data = UserResponseSerializer(many=True)

class SuccessGetChannelListSerializer(serializers.Serializer):
    message = serializers.CharField()
    data = ChannelSerializer(many=True)
    
class SuccessGetUserProfileSerializer(serializers.Serializer):
    message = serializers.CharField()
    data = UserProfileSerializer()
    
class SuccessUpdateUserProfileSerializer(serializers.Serializer):
    message = serializers.CharField()
    data = UserProfileSerializer()
    
class SuccessUploadAvatarSerializer(serializers.Serializer):
    message = serializers.CharField()
    data = inline_serializer(
        name="dataSuccessUploadAvatarSerializer",
        fields={
            "avatar_url": serializers.URLField()
        }
    )
    
class FileUploadSerializer(serializers.Serializer):
    file = serializers.ImageField()
    
class SuccessGetFriendListSerializer(serializers.Serializer):
    message = serializers.CharField()
    data = UserWithoutEmailSerializer(many=True)
    
class SuccessGetNotificationListSerializer(serializers.Serializer):
    message = serializers.CharField()
    data = NotificationSerializer(many = True)