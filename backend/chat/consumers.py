import json
from .async_db import *   
from channels.generic.websocket import AsyncWebsocketConsumer


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



    # text_json_data = {
    #     "data_type": DATA_TYPE,
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
                self.groupName, {"type": "chat.send", "text_data_json": text_data_json}
            )
        except Exception as e:
            print(e)
        

    async def dbAsyncHandle(self, text_data_json):
        data_type = text_data_json.get('data_type')
        action = text_data_json.get('action')
        data = text_data_json.get('data')

        if data_type == DATA_TYPE.MESSAGE:
            if action == ACTION.CREATE:
                return await createMessage(data)
            if action == ACTION.UPDATE:
                return await updateMessage(data)
            if action == ACTION.DELETE:
                return await deleteMessage(data)
        if data_type == DATA_TYPE.REACTION:
            if action == ACTION.CREATE:
                return await createReaction(data)
            if action == ACTION.UPDATE:
                return await updateReaction(data)
            if action == ACTION.DELETE:
                return await deleteReation(data)


    # Receive message from group
    async def chat_send(self, event):
        text_data_json = event["text_data_json"]
        text_data = json.dumps(text_data_json)

        # Send message to WebSocket
        await self.send(text_data=text_data)