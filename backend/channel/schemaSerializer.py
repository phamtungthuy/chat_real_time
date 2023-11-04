from rest_framework import serializers
from drf_spectacular.utils import inline_serializer
from .serializer import MemberSerializer
from user.serializer import UserSerializer


class CreateChannelRequestSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    members = serializers.ListField(
        child=serializers.IntegerField()
    )