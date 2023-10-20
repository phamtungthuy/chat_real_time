from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Friend, Notification
from drf_spectacular.utils import extend_schema_serializer
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'avatar_url', 'password', 'email', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def get_avatar_url(self, obj):
        return obj.profile.avatar_url

    def to_representation(self, instance):
        data = super(UserSerializer, self).to_representation(instance)
        data['fullname'] = f'{instance.first_name} {instance.last_name}'
        return data

    def get(self):
        data = self.data
        data.pop('email')
        return data

    def create(self, validated_data):
        required_fields = ['username', 'password', 'email', 'first_name', 'last_name']
        if any(key not in validated_data.keys() for key in required_fields):
            raise serializers.ValidationError('Info must be provided fully') 
        user = User.objects.create(**validated_data)
        UserProfile.objects.create(user=user)
        return user

    def validate_username(self, value):
        if len(value) < 6:
            raise serializers.ValidationError('Username must be at least 6 characters')
        elif any(not c.isalnum() for c in value):
            raise serializers.ValidationError('Username must only include alphabet letters')
        elif User.objects.filter(username=value):
            raise serializers.ValidationError('Username had been used')
        return value
    
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('Password must be at least 8 characters')
        elif ' ' in value:
            raise serializers.ValidationError('Password must not contain a blank')
        return make_password(value)
    
    def validate_email(self, value):
        users = User.objects.filter(email=value)
        if users:
            for user in users:
                userProfile = UserProfile.objects.get(user=user)
                if userProfile.verified:
                    raise serializers.ValidationError('Email had been used')
        return value

    def validate_first_name(self, value):
        if not value or any(not c.isalpha() for c in value):
            raise serializers.ValidationError("First name must only include alphabet letters")
        return value

    def validate_last_name(self, value):
        if not value or any(not c.isalpha() for c in value):
            raise serializers.ValidationError("Last name must only include alphabet letters")
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'bio', 'avatar_url', 'phone_number', 'address', 'online']
    
    def update(self, instance, validated_data):
        instance.bio = validated_data.get('bio', instance.bio)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.address = validated_data.get('address', instance.address)
        instance.save()
        return instance

    def getFriendProfile(self):
        data = self.data
        data.pop("address", None)
        return data

    def getStrangerProfile(self):
        data = self.data
        data.pop('phone_number', None)
        data.pop('address', None)
        data.pop('online', None)
        return data


class FriendSerializer(serializers.ModelSerializer):
    friend = serializers.SerializerMethodField()

    class Meta:
        model = Friend
        fields = ['friend']

    def get_friend(self, obj):
        friendSerializer = UserSerializer(obj.friend_with, many=False)
        data = friendSerializer.get()
        return data
    
    def to_representation(self, instance):
        data = super(FriendSerializer, self).to_representation(instance)
        return data['friend']


class NotificationSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['sender', 'notification_type', 'create_at', 'receiver']
        extra_kwargs = {
            'receiver': {'write_only': True}
        }

    def get_sender(self, obj):       
        senderSerializer = UserSerializer(obj.sender, many=False)
        data = senderSerializer.get()
        return data
