from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Message, Reaction, Emoji
from .serializer import MessageSerializer, ReactionSerializer, EmojiSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .schema import *
from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Message'])
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    permission_classes = [AllowAny]
    serializer_class = MessageSerializer

    
    @getMessageListSchema
    def getMessageList(self, request, channelId):
        try:
            messageList = queryset.filter(channel=channelId)
            serializer = serializer_class(messageList, many=True)
            return Response({'message': 'Get message list successfully', 'data': serializer.data})
        except:
            return Response({'message': 'Channel not found'}, status=status.HTTP_404_NOT_FOUND)


    @createMessageSchema
    def createMessage(self, request):
        data = request.data
        serializer = serializer_class(data=data)
        serializer.save()
        return Response({'message': 'Create message successfully', 'data': serializer.data})


    @editMessageSchema
    def editMessage(self, request, messageId):
        content = request.data.get('content')
        try:
            message = queryset.get(pk=messageId)
            message.content = content
            message.save()
            serializer = serializer_class(message, many=False)
            return Response({'message': 'Edit message successfully', 'data': serializer.data})
        except:
            return Response({'message': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)


    @deleteMessageSchema
    def deleteMessage(self, request, messageId):
        try:
            message = queryset.get(pk=messageId)
            message.delete()
            Response({'message': 'Delete message successfully'})
        except:
            Response({'message': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)


@extend_schema(tags=['Reaction'])
class ReactionViewSet(viewsets.ModelViewSet):
    queryset = Reaction.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ReactionSerializer


    @createReactionSchema
    def createReaction(self, request):
        data = request.data
        serializer = serializer_class(data=data)
        serializer.save()
        return Response({'message': 'Create reaction successfully', 'data': serializer.data})


    @getReactionListSchema
    def getReactionList(self, request, messageId):
        try:
            reactionList = queryset.filter(message=messageId)
            serializer = serializer_class(reactionList, many=True)
            return Response({'message': 'Get reaction list successfully', 'data': serializer.data})
        except:
            return Response({'message': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)


    @changeReactionSchema
    def changeReaction(self, request, reactionId):
        try:
            reaction = queryset.get(pk=reactionId)
            reaction.emoji = request.data.get('emoji')
            reaction.save()
            serializer = ReactionSerializer(reaction, many=False)
            return Response({'message': 'Change reaction successfully', 'data': serializer.data})
        except:
            return Response({'message': 'Reaction not found'}, status=status.HTTP_404_NOT_FOUND)


    @removeReactionSchema
    def removeReaction(self, request, reactionId):
        try:
            reaction = queryset.get(pk=reactionId)
            reaction.delete()
            Response({'message': 'Remove reaction successfully'})
        except:
            Response({'message': 'Reaction not found'}, status=status.HTTP_404_NOT_FOUND)



@extend_schema(tags=['Emoji'])
@getEmojiListSchema
@api_view(['GET'])
def getEmojiList(request):
    emojiList = Emoji.objects.all()
    serializer = EmojiSerializer(emojiList, many=True)
    return Response({'message': 'Get emoji list successfully', 'data': serializer.data})