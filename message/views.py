from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Message, Reaction, Emoji
from .serializer import MessageSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .schema import *

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
            return Response({'message': 'Get message list successful', 'data': serializer.data})
        except:
            return Response({'message': 'Channel not found'}, status=status.HTTP_404_NOT_FOUND)


    @createMessageSchema
    def createMessage(self, request):
        data = request.data
        serializer = serializer_class(data=data)
        serializer.save()
        return Response({'message': 'Create message successful', 'data': serializer.data})


    @editMessageSchema
    def editMessage(self, request, messageId):
        content = request.data.get('content')
        try:
            message = queryset.get(pk=messageId)
            message.content = content
            message.save()
            serializer = serializer_class(message, many=False)
            return Response({'message': 'Edit message successful', 'data': serializer.data})
        except:
            return Response({'message': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)


    @deleteMessageSchema
    def deleteMessage(self, request, messageId):
        try:
            message = queryset.get(pk=messageId)
            message.delete()
            Response({'message': 'Delete message successful'})
        except:
            Response({'message': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)
