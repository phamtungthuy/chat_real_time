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

getAllChannelsSchema = extend_schema(
    summary = "Get information of all channels",
    description="Require access token and permission to make this action",
    responses = {
        200: OpenApiResponse(response=SuccessGetAllChannelsSerializer,
                             description="Get all channels successfully"),
        401: OpenApiResponse(response=GeneralMessageSerializer, 
                             description="You need to provide access token and permission from admin to make this action")
        
        
    }
)

deleteChannelSchema = extend_schema(
    summary= "Delete a particular schema",
    description="You need permission to delete channel \n\n \
        Using websocker if you want to delete channel",
    responses= {
        200: OpenApiResponse(response=GeneralMessageSerializer,
                             description="Delete the channel successfully"),
        401: OpenApiResponse(response=GeneralMessageSerializer,
                             description="You need to provide access token and permission from admin to make this action"),
        404: OpenApiResponse(response=GeneralMessageSerializer,
                             description="Channel not found")
    }
        
)

createChannelSchema = extend_schema(
    summary= 'Create channel',
    description = 'Require access token to make this action \n\n \
        Using websocket to create channel',
    request = CreateChannelRequestSerializer,
    responses= {
        200: OpenApiResponse(response=SuccessCreateChannelSerializer, 
                             description="Create channel successfully"),
        400: OpenApiResponse(response=GeneralMessageSerializer,
                             description="Error when creating channel"),
        401: OpenApiResponse(response=GeneralMessageSerializer, 
                             description="You need to provide access token from admin to make this action")
    }
)

getMediaListSchema = extend_schema(
    summary="Get all media",
    description= "Require access token to make this action",
    responses= {
        200: OpenApiResponse(response = SuccessGetMediaListSerializer,
                             description="Get all media of the channel successfully"),
        401: OpenApiResponse(response=GeneralMessageSerializer, 
                             description="You need to provide access token from admin to make this action"),
        404: OpenApiResponse(response=GeneralMessageSerializer,
                             description="Channel not found"),
    }    
)

getMemberListSchema = extend_schema(
    summary="Get all members of the channel",
    description= "Require access token to make this action",
    responses= {
        200: OpenApiResponse(response=SuccessGetMemberListSerializer,
                             description="Get all members of the channel"),
        401: OpenApiResponse(response=GeneralMessageSerializer, 
                             description="You need to provide access token from admin to make this action"),
        404: OpenApiResponse(response=GeneralMessageSerializer,
                             description="Channel not found"),
    }
)

uploadChannelAvatarSchema = extend_schema(
    summary="Upload the channel avatar",
    description= "Require access token to make this action \n\n \
        Using websocket to make this action",
    request= inline_serializer(
        name="uploadChannelAvatarRequest",
        fields={
            "file": serializers.FileField(),
            "channel": serializers.IntegerField()
        }
    ),
    responses = {
        200: OpenApiResponse(response=SuccessUploadChannelAvatarSerializer,
                             description="Upload avatar successfully"),
        400: OpenApiResponse(response=GeneralMessageSerializer,
                             description="Error when uploading image"),
        401: OpenApiResponse(response=GeneralMessageSerializer, 
                             description="You need to provide access token from admin to make this action"),
        404: OpenApiResponse(response=GeneralMessageSerializer,
                             description="Channel not found"),
        413: OpenApiResponse(response=GeneralMessageSerializer,
                             description="Image too large"),
        415: OpenApiResponse(response=GeneralMessageSerializer,
                             description="File type not supported")
    }
)