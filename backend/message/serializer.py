from rest_framework import serializers
from .models import Message, Emoji, Reaction
from channel.serializer import MemberSerializer

class MessageSerializer(serializers.ModelSerializer):
    member = MemberSerializer()

    class Meta:
        model = Message
        fields = '__all__'


class EmojiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emoji
        fields = '__all__'
        

class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = '__all__'
