from rest_framework.serializers import ModelSerializer
from .models import Message, Emoji, Reaction

class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class EmojiSerializer(ModelSerializer):
    class Meta:
        model = Emoji
        fields = '__all__'

class ReactionSerializer(ModelSerializer):
    class Meta:
        model = Reaction
        fields = '__all__'
