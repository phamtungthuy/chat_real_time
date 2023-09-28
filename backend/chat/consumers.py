import json
from .async_db import *   
from rest_framework.exceptions import ValidationError
from channels.generic.websocket import AsyncWebsocketConsumer
from user.models import UserProfile
from django.contrib.auth.models import AnonymousUser


class LobbyConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def setOnlineUser(self, user):
        userProfile = UserProfile.objects.get(user=user)
        userProfile.online = True
        userProfile.save()

    @database_sync_to_async
    def setOfflineUser(self, user):
        userProfile = UserProfile.objects.get(user=user)
        userProfile.online = False
        userProfile.save()

    @database_sync_to_async
    def getOnlineUser(self):
        onlineUser = UserProfile.objects.filter(online=True)
        return onlineUser


    async def connect(self):
        # Change online status
        self.user = self.scope['user']
        await self.setOnlineUser(self.user)

        # Join room group
        await self.channel_layer.group_add('onlineUser', self.channel_name)
        await self.accept()


    async def disconnect(self, close_code):
        # Change offline status
        await self.setOnlineUser(self.user)

        # Leave room group
        await self.channel_layer.group_discard('onlineUser', self.channel_name)


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message}
        )


    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join chat room
        print(self.scope['user'])
        self.chatRoomId = self.scope["url_route"]["kwargs"]["chatRoomId"]
        self.group_name = f'group_{self.chatRoomId}'
        # Check if user is authenticated
        if self.scope['user'].is_anonymous:
            return await self.close(code=1000)
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

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
            text_data_json['data'] = await self.dbAsyncHandle(text_data_json)
            # Send message to group
            await self.channel_layer.group_send(
                self.group_name, {"type": "chat.send", "text_data_json": text_data_json}
            )
        except ValidationError as e:
            print(e)
            return await self.close(code=1000)


    # Receive message from group
    async def chat_send(self, event):
        text_data_json = event["text_data_json"]
        text_data = json.dumps(text_data_json)

        # Send message to WebSocket
        await self.send(text_data=text_data)

    
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
            return await deleteReaction(data)
        if action == ACTION.ADD_MEMBER:
            return await addMember(data)
        if action == ACTION.REMOVE_MEMBER:
            return await removeMember(data)