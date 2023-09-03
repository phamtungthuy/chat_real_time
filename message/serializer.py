from rest_framework.serializers import ModelSerializer
from .models import Message, Emoji, Reaction

class MessageSeriazlier(ModelSerializer):
    class Meta:
        models = Message
        fields = '__all__'

class EmojiSerializer(ModelSerializer):
    class Meta:
        models = Emoji
        fields = '__all__'

class ReactionSerializer(ModelSerializer):
    class Meta:
        models = Reaction
        fields = '__all__'
