from rest_framework import serializers
from .serializer import *

class GeneralMessageSerializer(serializers.Serializer):
    message = serializers.CharField()

class SuccessCreateMessageSerializer(serializers.Serializer):
    message = serializers.CharField()
    data = MessageSerializer()

class SuccessEditMessageSerializer(serializers.Serializer):
    message = serializers.CharField()
    data = MessageSerializer()


class UploadImageMessageRequestSerializer(MessageSerializer):
    file = serializers.ListField(
        child = serializers.ImageField()
    )
    class Meta:
        model=Message
        fields = ["file", "message_type","content","member","channel","reply"]