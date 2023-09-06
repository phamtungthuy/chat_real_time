import json
from message.models import Message
from message.serializer import MessageSerializer
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import sys

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.groupId = self.scope["url_route"]["kwargs"]["groupId"]
        self.groupName = f'group_{self.groupId}'
        # Join group
        await self.channel_layer.group_add(self.groupName, self.channel_name)
        await self.accept()


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.groupName, self.channel_name)


    # Receive message from WebSocket
    async def receive(self, text_data):
        try:
            message = {
                'content': json.loads(text_data).get('content'),
                'member': 3, #self.scope['user'].id
                'channel': self.groupId
            }
            await self.save_message(message)

            # Send message to group
            await self.channel_layer.group_send(
                self.groupName, {"type": "chat.message", "message": message}
            )
        except:
            pass
        

    @database_sync_to_async
    def save_message(self, data):
        serializer = MessageSerializer(data=data)
        if (serializer.is_valid()):
            serializer.save()
        else:
            print(serializer.errors.items())


    # Receive message from group
    async def chat_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))