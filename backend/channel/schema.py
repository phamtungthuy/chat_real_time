from drf_spectacular.utils import extend_schema, OpenApiResponse, inline_serializer
from rest_framework import serializers
from message.serializer import MessageSerializer

getMessageListSchema = extend_schema(
    summary = 'Get message list by channel id',
    responses = {
        200: OpenApiResponse(response=MessageSerializer(many=True),
                             description="Get message list successfully"),
        404: OpenApiResponse(description="Channel not found")
    }
)