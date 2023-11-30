from rest_framework import serializers
from .serializer import *

class GeneralMessageSerializer(serializers.Serializer):
    message = serializers.CharField()

class SearchChannelResponse(serializers.Serializer):
    users = SearchUserSerializer(many=True)
    channels = SearchChannelSerializer(many=True)
    resultSize = serializers.IntegerField()

class SearchMessageResponse(serializers.Serializer):
    messages = SearchMessageSerializer(many=True)
    resultSize = serializers.IntegerField()

class SearchFriendResponse(serializers.Serializer):
    friends = SearchUserSerializer(many=True)
    resultSize = serializers.IntegerField()