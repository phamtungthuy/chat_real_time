from drf_spectacular.utils import extend_schema, OpenApiResponse, inline_serializer
from rest_framework import serializers
from message.serializer import MessageSerializer
from .serializer import ChannelSerializer
from .schemaSerializer import *
getMessageListSchema = extend_schema(
    summary = 'Get message list by channel id',
    responses = {
        200: OpenApiResponse(response=MessageSerializer(many=True),
                             description="Get message list successfully"),
        404: OpenApiResponse(description="Channel not found")
    }
)

createChannelSchema = extend_schema(
    summary= 'Create channel',
    request = CreateChannelRequestSerializer
)