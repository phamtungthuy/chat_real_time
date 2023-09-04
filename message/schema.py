from drf_spectacular.utils import extend_schema, OpenApiResponse, inline_serializer
from rest_framework import serializers
from .serializer import MessageSerializer

getMessageListSchema = extend_schema(
    summary = 'Get message list by channel id',
    responses = {
        200: OpenApiResponse(response=MessageSerializer(many=True),
                             description="Get message list successful"),
        404: OpenApiResponse(description="Channel not found")
    }
)

createMessageSchema = extend_schema(
    summary = 'Create message',
    request = MessageSerializer,
    responses = {
        200: OpenApiResponse(response=MessageSerializer,
                             description="Create message successfully")
    }
)

editMessageSchema = extend_schema(
    summary = "Edit message",
    request = inline_serializer(
        name = 'EditMessageRequest',
        fields = {
            'id': serializers.IntegerField(),
            'content': serializers.CharField()
        }
    ),
    responses = {
        200: OpenApiResponse(response=MessageSerializer, description="Edit message successful"),
        404: OpenApiResponse(description="Message not found")
    }
)


deleteMessageSchema = extend_schema(
    summary = 'Delete message',
    responses = {
        200: OpenApiResponse(description="Delete message successful"),
        404: OpenApiResponse(description="Message not found")
    }
)
