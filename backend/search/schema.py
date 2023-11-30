from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter, inline_serializer
from rest_framework import serializers
from .schemaSerializer import SearchChannelResponse, SearchMessageResponse, SearchFriendResponse, GeneralMessageSerializer

searchChannelSchema = extend_schema(
    tags = ['Search'],
    summary = 'Search channel (user you was chatted with, and channel you joined)',
    parameters = [
        OpenApiParameter(
            'query'
        )
    ],
    responses = {
        200: OpenApiResponse(response=SearchChannelResponse,
                             description="Search channel successfully"),
    }
)

searchMessageSchema = extend_schema(
    tags = ['Search'],
    summary = 'Search message in your channel',
    parameters = [
        OpenApiParameter(
            'query'
        )
    ],
    responses = {
        200: OpenApiResponse(response=SearchMessageResponse,
                             description="Search message successfully"),
        403: OpenApiResponse(response=GeneralMessageSerializer,
                             description="You are not member of this channel"),
        404: OpenApiResponse(response=GeneralMessageSerializer,
                             description="Channel not found"),
    }
)

searchFriendSchema = extend_schema(
    tags = ['Search'],
    summary = 'Search user in your friend list',
    parameters = [
        OpenApiParameter(
            'query'
        )
    ],
    responses = {
        200: OpenApiResponse(response=SearchFriendResponse,
                             description="Search friend successfully"),
    }
)