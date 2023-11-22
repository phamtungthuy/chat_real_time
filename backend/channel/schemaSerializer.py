from rest_framework import serializers
from drf_spectacular.utils import inline_serializer
from .serializer import *
from message.serializer import MessageSerializer
from user.serializer import UserSerializer

class GeneralMessageSerializer(serializers.Serializer):
    message = serializers.CharField()

class CreateChannelRequestSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    members = serializers.ListField(
        child=serializers.IntegerField()
    )
    
class SuccessGetAllChannelsSerializer(serializers.Serializer):
    message = serializers.CharField()
    data = ChannelSerializer(many=True)

class SuccessCreateChannelSerializer(serializers.Serializer):
    message = serializers.CharField()
    data = ChannelSerializer()
    
class SuccessGetMediaListSerializer(serializers.Serializer):
    message = serializers.CharField()
    data = MessageSerializer(many=True)
    
class SuccessGetMemberListSerializer(serializers.Serializer):
    message = serializers.CharField()
    data = MemberSerializer(many=True)
    
class SuccessUploadChannelAvatarSerializer(serializers.Serializer):
    message = serializers.CharField()
    data = inline_serializer(
        name="UploadChannelAvatar",
        fields={
            "avatar_url": serializers.CharField(),
            "channel": serializers.IntegerField()
        }
    )
