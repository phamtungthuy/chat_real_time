import json
from .async_db import *   
from channels.generic.websocket import AsyncWebsocketConsumer
from user.models import UserProfile


class ChatConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def onlineUser(self, user):
        userProfile = UserProfile.objects.get(user=user)
        userProfile.online = True
        userProfile.save()

    @database_sync_to_async
    def offlineUser(self, user):
        userProfile = UserProfile.objects.get(user=user)
        userProfile.online = False
        userProfile.save()


    async def connect(self):
        # Change online status
        # self.user = self.scope['user']
        # await self.onlineUser(self.user)

        # Join chat room
        self.chatRoomId = self.scope["url_route"]["kwargs"]["chatRoomId"]
        await self.channel_layer.group_add(self.chatRoomId, self.channel_name)
        await self.accept()


    async def disconnect(self, close_code):
        # Change offline status
        # await self.offlineUser(self.user)

        # Leave room group
        await self.channel_layer.group_discard(self.chatRoomId, self.channel_name)


    # text_json_data = {
    #     "action": ACTION,
    #     "data": {
    #         "member": member,
    #         "channel": channel,
    #         ...
    #     }
    # }

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        try:
            serializerData = await self.dbAsyncHandle(text_data_json)
            text_data_json['data'] = serializerData
            # Send message to group
            await self.channel_layer.group_send(
                self.chatRoomId, {"type": "chat.send", "text_data_json": text_data_json}
            )
        except Exception as e:
            print(e)
        

    async def dbAsyncHandle(self, text_data_json):
        action = text_data_json.get('action')
        data = text_data_json.get('data')

        if action == ACTION.CREATE_MESSAGE:
            return await createMessage(data)
        if action == ACTION.DELETE_MESSAGE:
            return await deleteMessage(data)
        if action == ACTION.CREATE_REACTION:
            return await createReaction(data)
        if action == ACTION.DELETE_REACTION:
            return await deleteReation(data)


    # Receive message from group
    async def chat_send(self, event):
        text_data_json = event["text_data_json"]
        text_data = json.dumps(text_data_json)

        # Send message to WebSocket
        await self.send(text_data=text_data)