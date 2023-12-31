import json
from chat import async_db
from .async_db import ACTION, TARGET
from rest_framework.exceptions import ValidationError
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from channels.exceptions import StopConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Check if user is authenticated
        if self.scope['user'].is_anonymous:
            await self.accept()
            return await self.close(code=3000)
        else:
            self.user = self.scope['user']
        # Set online status
        await async_db.setOnlineUser(self.user)
        # Join all chat group
        channels = await async_db.getUserChannels(self.user)
        for channel in channels:
            group_name = f'group_{channel.id}'
            await self.channel_layer.group_add(group_name, self.channel_name)
        # Set a group for only user
        await self.channel_layer.group_add(f'user_{self.user.id}', self.channel_name)
        # Accept ws connect
        await self.accept()


    async def disconnect(self, close_code):
        if close_code == 3000:
            return
        # Change offline status
        await async_db.setOfflineUser(self.user)
        # Leave all chat group
        # channels = await async_db.getUserChannels(self.user)
        # if channels is not None:
        #     for channel in channels:
        #         group_name = f'group_{channel.id}'
        #         await self.channel_layer.group_discard(group_name, self.channel_name)
        raise StopConsumer()


    # Receive message from WebSocket
    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            text_data_json['data'] = await self.dbAsyncHandle(text_data_json)
            target = text_data_json.get('target', '')

            # Not target -> not send ws

            # Send message to user
            if target == TARGET.USER:
                userId = text_data_json['targetId']
                await self.channel_layer.group_send(
                    f'user_{userId}', {"type": "chat.send", "text_data_json": text_data_json}
                )
            # Send message to group
            elif target == TARGET.CHANNEL:
                channelId = text_data_json['targetId']
                await self.channel_layer.group_send(
                    f'group_{channelId}', {"type": "chat.send", "text_data_json": text_data_json}
                )
        except Exception as e:
            text_data = json.dumps({"error_message": repr(e)})
            # Send error message to user send
            await self.send(text_data=text_data)


    # Receive message from group
    async def chat_send(self, event):
        text_data_json = event["text_data_json"]
        text_data = json.dumps(text_data_json)
        # Send message to WebSocket
        await self.send(text_data=text_data)

    async def joinChannel(self):
        channels = await async_db.getUserChannels(self.user)
        for channel in channels:
            group_name = f'group_{channel.id}'
            await self.channel_layer.group_add(group_name, self.channel_name)

    async def dbAsyncHandle(self, text_data_json):
        action = text_data_json.get('action', None)
        targetId = text_data_json.get('targetId', None)
        data = text_data_json.get('data', {})

        """
            {
                action: 'join_channel',
                target: 'channel',
                targetId: channelId
            }
        """

        # Join channel
        if action == ACTION.JOIN_CHANNEL:
            await self.joinChannel()
            await self.send(text_data="Join channel successfully")

        # Member, creator action
        if action == ACTION.CREATE_MESSAGE:
            return await async_db.createMessage(self.user, targetId, data)
        if action == ACTION.REMOVE_MESSAGE:
            return await async_db.removeMessage(data)
        if action == ACTION.CREATE_REACTION:
            return await async_db.createReaction(self.user, targetId, data)
        if action == ACTION.REMOVE_REACTION:
            return await async_db.removeReaction(data)
        if action == ACTION.OUT_CHANNEL:
            return await async_db.outChannel(self.user, targetId, data)
        if action == ACTION.SET_NICKNAME:
            return await async_db.setNickname(data)
        if action == ACTION.REMOVE_NICKNAME:
            return await async_db.removeNickname(data)
        if action == ACTION.FRIEND_REQUEST:
            return await async_db.friendRequest(self.user, targetId, data)
        if action == ACTION.FRIEND_ACCEPT:
            return await async_db.friendAccept(self, targetId, data)
        if action == ACTION.FRIEND_DENY:
            return await async_db.friendDeny(self.user, targetId)


        if (await async_db.isCreator(self.user, targetId)):
            if action == ACTION.ADD_MEMBER:
                return await async_db.addMember(targetId, data)
            if action == ACTION.REMOVE_MEMBER:
                return await async_db.removeMember(data)
            if action == ACTION.SET_CHANNEL_TITLE:
                return await async_db.setChannelTitle(targetId, data)
            if action == ACTION.CHANGE_CREATOR:
                return await async_db.changeCreator(self.user, data)
            if action == ACTION.DISBAND_CHANNEL:
                return await async_db.disbandChannel(targetId, data)
        else:
            raise Exception("User is not creator to perform this action")

        return data