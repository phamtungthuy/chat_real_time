from rest_framework.serializers import ModelSerializer
from .models import Channel, Member

class ChannelSerializer(ModelSerializer):
    class Meta:
        model = Channel
        fields = '__all__'

class MemberSerializer(ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'
