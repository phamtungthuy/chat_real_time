from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Friend, Notification
from drf_spectacular.utils import extend_schema_serializer
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password, check_password

class UserListSerializer(serializers.ListSerializer):
    def get(self):
        data_set = self.data
        for i, data in enumerate(data_set):
            data_set[i].pop('password', None)
        return data_set

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']
        list_serializer_class = UserListSerializer
    
    def validate(self, data):
        if self.instance is not None:
            return data
        if any(field not in data for field in ['username', 'email', 'password']):
            raise serializers.ValidationError('Username, email and password must be provided')
        return data

    def validate_username(self, value):
        if len(value) < 3:
            raise serializers.ValidationError('Username must be at least 3 characters')
        elif ' ' in value:
            raise serializers.ValidationError('Username must not contain a blank')
        elif User.objects.filter(username=value):
            raise serializers.ValidationError('Username had been used')
        return value
    
    def validate_password(self, value):
        if len(value) < 7:
            raise serializers.ValidationError('Password must be at least 7 characters')
        elif ' ' in value:
            raise serializers.ValidationError('Password must not contain a blank')
        return make_password(value)
    
    def validate_email(self, value):
        if ' ' in value:
            raise serializers.ValidationError('Email must not contain a blank')
        users = User.objects.filter(email=value)
        if users:
            for user in users:
                userProfile = UserProfile.objects.get(user=user)
                if userProfile.verified:
                    raise serializers.ValidationError('Email had been used')
        return value
    
    def get(self):
        data = self.data
        data = {
            "username": data['username'],
            "email": data['email']
        }
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=False)
    verification_code = serializers.CharField(required=False)

    class Meta:
        model = UserProfile
        fields = '__all__'

    def to_representation(self, instance):
        data = super(UserProfileSerializer, self).to_representation(instance)
        data.pop('user', None)
        data.pop('verified', None)
        data.pop('verification_code', None)
        return data
    
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
            'avatar_url': data['avatar_url'],
            'fullname': data['fullname']
        }


class FriendSerializer(serializers.ModelSerializer):
    friend_with = serializers.SerializerMethodField()

    def get_friend_with(self, obj):
        friendProfile = UserProfile.objects.get(user=obj.friend_with)
        friendProfileSerializer = UserProfileSerializer(friendProfile, many=False)
        data = friendProfileSerializer.getFriendProfile()
        data['username'] = obj.friend_with.username
        return data
    
    class Meta:
        model = Friend
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'