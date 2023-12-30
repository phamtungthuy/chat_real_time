from rest_framework import serializers
from channel.models import Channel
from django.contrib.auth.models import User
from user.serializer import UserSerializer
from message.serializer import MessageSerializer

class SearchChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = '__all__'


class SearchUserSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()
    avatar_url = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'id', 'avatar_url', 'fullname']

    def get_fullname(self, obj):
        return obj.first_name + " " + obj.last_name 

    def get_avatar_url(self, obj):
        return obj.profile.avatar_url

class SearchMessageSerializer(MessageSerializer):
    pass