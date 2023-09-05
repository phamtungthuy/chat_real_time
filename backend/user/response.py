from rest_framework import serializers
from drf_spectacular.utils import inline_serializer

class UserResponseSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.CharField()

class ResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    
class SuccessResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    data = UserResponseSerializer()