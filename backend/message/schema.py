from drf_spectacular.utils import extend_schema, OpenApiResponse, inline_serializer
from rest_framework import serializers
from .serializer import MessageSerializer, ReactionSerializer, EmojiSerializer
from .schemaSerializer import *
# Message schema

createMessageSchema = extend_schema(
    summary = 'Create message',
    description="You need provide access token to create a message to send",
    request = MessageSerializer,
    responses = {
        200: OpenApiResponse(response=SuccessCreateMessageSerializer,
                             description="Create message successfully"),
        400: OpenApiResponse(response=GeneralMessageSerializer, description='Have some problems when creating message'),
        401: OpenApiResponse(response=GeneralMessageSerializer, description="You need to provide access token to make this action")
    }
)

uploadImageSchema = extend_schema(
    summary= "Upload image in conversation",
    description = "You need to provided access token to make this action",
    request=UploadImageMessageRequestSerializer
)

editMessageSchema = extend_schema(
    summary = "Edit message",
    description="You need provided access token to edit a particular message",
    request = inline_serializer(
        name = 'editMessageRequestSerializer',
        fields = {
            'content': serializers.CharField()
        }
    ),
    responses = {
        200: OpenApiResponse(response=SuccessEditMessageSerializer, description="Edit message successfully"),
        400: OpenApiResponse(response=GeneralMessageSerializer, description="Have some problesm while editing message!"),
        401: OpenApiResponse(response=GeneralMessageSerializer, description="You need to provided access token to make this action"),
        404: OpenApiResponse(response=GeneralMessageSerializer, description="Message not found")
    }
)

deleteMessageSchema = extend_schema(
    summary = 'Delete message',
    description="You need to provide access token to delete a particular message",
    responses = {
        200: OpenApiResponse(response=GeneralMessageSerializer, description="Delete message successfully"),
        401: OpenApiResponse(response=GeneralMessageSerializer, description="You need to provided access token to make this action"),
        404: OpenApiResponse(response=GeneralMessageSerializer, description="Message not found")
    }
)


# Reaction schema

getReactionListSchema = extend_schema(
    summary = 'Get reaction list by message id',
    responses = {
        200: OpenApiResponse(response=ReactionSerializer(many=True),
                             description="Get reaction list successfully"),
        404: OpenApiResponse(description="Message not found")
    }
)

createReactionSchema = extend_schema(
    summary = 'Create reaction',
    request = ReactionSerializer,
    responses = {
        200: OpenApiResponse(response=ReactionSerializer,
                             description="Create reaction successfully"),
        400: OpenApiResponse(description='Bad request')
    }
)

changeReactionSchema = extend_schema(
    summary = "Change reaction",
    request = inline_serializer(
        name = 'changeReactionSchema',
        fields = {
            'emoji': serializers.IntegerField()
        }
    ),
    responses = {
        200: OpenApiResponse(response=ReactionSerializer, description="Edit message successfully"),
        400: OpenApiResponse(description='Bad request'),
        404: OpenApiResponse(description="Message not found")
    }
)

removeReactionSchema = extend_schema(
    summary = 'Remove reaction',
    responses = {
        200: OpenApiResponse(description="Remove reaction successfully"),
        404: OpenApiResponse(description="Message not found")
    }
)


# Emoji schema

getEmojiListSchema = extend_schema(
    summary = 'Get emoji list',
    responses =  {
        200: OpenApiResponse(response=EmojiSerializer(many=True), description='Get emoji list successfully')
    }
)