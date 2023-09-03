from rest_framework.serializers import ModelSerializer
from .models import Channel, Memeber

class ChannelSeriazlier(ModelSerializer):
    class Meta:
        models = Channel
        fields = '__all__'

class MemberSerializer(ModelSerializer):
    class Meta:
        models = Member
        fields = '__all__'
