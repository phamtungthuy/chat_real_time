from rest_framework import serializers
from .models import Channel, Member
from user.serializer import UserSerializer
from message import serializer

class ChannelSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Channel
        fields = '__all__'
    
    def get_member_count(self, obj):
        return len(obj.members.all())

    def get_last_message(self, obj):
        last_message = obj.messages.all()[0]
        messageSerializer = serializer.MessageSerializer(last_message, many=False)
        return messageSerializer.data

    def validate_title(self, value):
        value = value.strip()
        if len(value) == 0:
            raise serializers.ValidationError('Title must not be blank')
        return value

    def update_title(self, title):
        self.instance.title = title
        self.instance.save()
        return self.instance


class MemberSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Member
        fields = '__all__'

    def get_user(self, obj):
        serializer = UserSerializer(obj.user, many=False)
        return serializer.get()

    def validate_nickname(self, value):
        value = value.strip()
        if len(value) == 0:
            raise serializers.ValidationError('Nickname must not be blank')
        return value
    
    def update_nickname(self, nickname):
        self.instance.nickname = nickname
        self.instance.save()
        return self.instance