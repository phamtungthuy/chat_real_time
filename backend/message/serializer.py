from rest_framework import serializers
from .models import Message, Emoji, Reaction
from channel.models import Member
import channel.serializer


class MessageSerializer(serializers.ModelSerializer):
    # member = channel.serializer.MemberSerializer()
    # member = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = '__all__'

    def to_representation(self, instance):
        data = super(MessageSerializer, self).to_representation(instance)
        memberSerializer = channel.serializer.MemberSerializer(instance.member, many=False)
        data['member'] = memberSerializer.data
        return data


class EmojiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emoji
        fields = '__all__'
        

class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = '__all__'
