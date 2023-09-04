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
            messageList = self.queryset.filter(channel=channelId)
            serializer = self.serializer_class(messageList, many=True)
            return Response({'message': 'Get message list successfully', 'data': serializer.data})
        except:
            return Response({'message': 'Channel not found'}, status=status.HTTP_404_NOT_FOUND)


    @createMessageSchema
    def createMessage(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Create message successfully', 'data': serializer.data})
        else:
            message = ''
            for key, value in serializer.errors.items():
                message += f'{value[0]} ({key})'
                break
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)


    @editMessageSchema
    def editMessage(self, request, messageId):
        try:
            message = self.queryset.get(pk=messageId)
        except:
            return Response({'message': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            message.content = request.data.get('content')
            message.save()
            serializer = self.serializer_class(message, many=False)
            return Response({'message': 'Edit message successfully', 'data': serializer.data})
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


    @deleteMessageSchema
    def deleteMessage(self, request, messageId):
        try:
            message = self.queryset.get(pk=messageId)
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
        serializer = self.serializer_class(data=data)
        if (serializer.is_valid(raise_exception=True)):
            serializer.save()
            return Response({'message': 'Create reaction successfully', 'data': serializer.data})
        else:
            message = ''
            for key, value in serializer.errors.items():
                message += f'{value[0]} ({key})'
                break
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)


    @getReactionListSchema
    def getReactionList(self, request, messageId):
        try:
            reactionList = self.queryset.filter(message=messageId)
            serializer = self.serializer_class(reactionList, many=True)
            return Response({'message': 'Get reaction list successfully', 'data': serializer.data})
        except:
            return Response({'message': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)


    @changeReactionSchema
    def changeReaction(self, request, reactionId):
        try:
            reaction = self.queryset.get(pk=reactionId)
        except:
            return Response({'message': 'Reaction not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            reaction.emoji = request.data.get('emoji')
            reaction.save()
            serializer = self.serializer_class(reaction, many=False)
            return Response({'message': 'Change reaction successfully', 'data': serializer.data})
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


    @removeReactionSchema
    def removeReaction(self, request, reactionId):
        try:
            reaction = self.queryset.get(pk=reactionId)
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