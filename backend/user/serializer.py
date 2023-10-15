from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Friend, Notification
from drf_spectacular.utils import extend_schema_serializer
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password, check_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def create(self, validated_data):
        required_fields = ['username', 'password', 'email', 'first_name', 'last_name']
        if any(key not in validated_data.keys() for key in required_fields):
            raise ValidationError('Info must be provided fully') 
        obj = User.objects.create(**validated_data)
        return obj

    def validate_username(self, value):
        if len(value) < 6:
            raise serializers.ValidationError('Username must be at least 6 characters')
        elif ' ' in value:
            raise serializers.ValidationError('Username must not contain a blank')
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


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'avatar_url', 'fullname', 'phone_number', 'address', 'online']
        extra_kwargs = {
            'verified': {'write_only': True},
            'verification_code': {'write_only': True}
        }
    
    def update(self, instance, validated_data):
        instance.fullname = validated_data.get('fullname', instance.fullname)
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
        return {
            'user': data['user'],
            'avatar_url': data['avatar_url'],
            'fullname': data['fullname']
        }


class FriendSerializer(serializers.ModelSerializer):
    friend = serializers.SerializerMethodField()

    class Meta:
        model = Friend
        fields = ['friend']

    def get_friend(self, obj):
        friend = UserProfile.objects.get(user=obj.friend_with)
        friendSerializer = UserProfileSerializer(friend, many=False)
        data = friendSerializer.getStrangerProfile()
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
        sender = UserProfile.objects.get(user=obj.sender)        
        senderSerializer = UserProfileSerializer(sender, many=False)
        data = senderSerializer.getStrangerProfile()
        return data
