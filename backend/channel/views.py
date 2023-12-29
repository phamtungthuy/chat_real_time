from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema
from .models import Channel, Member
from backend.pagination import MessagePagination
from .serializer import ChannelSerializer,MemberSerializer
from message.serializer import MessageSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.contrib.auth.models import User
from storages.backends.s3boto3 import S3Boto3Storage
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json, uuid
from .schema import *


@extend_schema(tags=['Channel'])
class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    pagination_class = MessagePagination

    def get_permissions(self):
        admin_actions = ['getAllChannels', 'deleteChannel']
        if self.action in admin_actions:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    @getAllChannelsSchema
    def getAllChannels(self, request):
        channels = self.queryset.all()
        serializer = self.serializer_class(channels, many=True)
        return Response({"message": "Get all channels successfully", "data": serializer.data})

    @deleteChannelSchema
    def deleteChannel(self, request, channelId):
        try:
            channel = self.queryset.get(pk=channelId)
            text_data_json = {
                "action": "delete_channel",
                "target": "channel",
                "targetId": channel.id,
                "data": {
                    "message": "Your channel has been deleted by admin"
                }
            }
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(f'group_{channelId}', {
                "type": "chat.send",
                "text_data_json": text_data_json
            })
            channel.delete()
            return Response({'message': 'Delete channel successfully'})
        except Channel.DoesNotExist:
            return Response({'message': 'Channel not found'}, status=status.HTTP_404_NOT_FOUND)

    @createChannelSchema
    def createChannel(self, request):
        data = request.data
        creator = request.user
        title = data.get('title')
        members = data.get('members')
        if len(members) < 3:
            return Response({"message": "A channel needs at least three members"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            channel = self.queryset.create(title=title)
            Member.objects.create(user=creator, channel=channel, role="CREATOR")
            for userId in members:
                Member.objects.create(user_id=userId, channel=channel)
            serializer = self.serializer_class(channel, many=False)
            # Send ws to all members
            text_data_json = {
                "action": "create_channel",
                "target": "channel",
                "targetId": channel.id,
                "data": serializer.data
            }
            channel_layer = get_channel_layer()
            # Send notification to all members who were added to new channel
            for userId in members:
                async_to_sync(channel_layer.group_send)(f'user_{userId}', {
                    "type": "chat.send",
                    "text_data_json": text_data_json
                })
            return Response({'message': 'Create channel successfully', 'data': serializer.data})
        except Exception as e:
            channel.delete()
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

    @getMediaListSchema
    def getMediaList(self, request, channelId):
        try:
            channel = self.queryset.get(pk=channelId)
            imageList = channel.messages.filter(message_type="IMAGE")
            serializer = MessageSerializer(imageList, many=True)
            return Response({"message": "Get media list successfully", "data": serializer.data}) 
        except Channel.DoesNotExist:
            return Response({'message': 'Channel not found'}, status=status.HTTP_404_NOT_FOUND)


    @getMemberListSchema
    def getMemberList(self, request, channelId):
        try:
            channel = self.queryset.get(pk=channelId)
            memberList = channel.members.all()
            serializer = MemberSerializer(memberList, many=True)
            return Response({'message': 'Get member list successfully', 'data': serializer.data})
        except Channel.DoesNotExist:
            return Response({'message': 'Channel not found'}, status=status.HTTP_404_NOT_FOUND)


    @getMessageListSchema
    def getMessageList(self, request, channelId):
        try:
            channel = self.queryset.get(pk=channelId)
            messageList = channel.messages.all()
            messageList = self.paginate_queryset(messageList)
            serializer = MessageSerializer(messageList, many=True)
            return self.get_paginated_response({'message': 'Get message list successfully', 'data': serializer.data})
            # return Response({'message': 'Get message list successfully', 'data': serializer.data})
        except Exception as e:
            print(repr(e))
            return Response({'message': 'Channel not found'}, status=status.HTTP_404_NOT_FOUND)


    @uploadChannelAvatarSchema
    def uploadChannelAvatar(self, request):
        file_obj = request.FILES.get('file')
        # Validate file
        if file_obj is None:
            return Response({"message": "File not provided"}, status=status.HTTP_400_BAD_REQUEST) 
        file_type = file_obj.content_type.split('/')[0]
        if file_type != 'image':
            return Response({"message": "File type not supported"}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        elif file_obj.size > 10**7:
            return Response({"message": "File size is too large"}, status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)
        # Upload file to s3
        data = request.data
        channelId = data.get('channel')
        try: 
            channel = Channel.objects.get(pk=channelId)
        except Channel.DoesNotExist:
            return Response({"message": "Channel not found"}, status=status.HTTP_404_NOT_FOUND)
        file_path = f'upload/channel/{channel}/avatar/{uuid.uuid4()}'
        s3 = S3Boto3Storage()
        s3.save(file_path, file_obj)
        file_url = s3.url(file_path)
        # Save to db as message
        data.pop('file', None)
        data['avatar_url'] = file_url
        try:
            channel.avatar_url = file_url
            channel.save()
            text_data_json = {
                "action": "upload_channel_avatar",
                "target": "channel",
                "targetId": channelId,
                "data": data['avatar_url']
            }
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(f'group_{channelId}', {
                "type": "chat.send",
                "text_data_json": text_data_json
            })
            return Response({"message": "Update channel avatar successfully", "data": data})
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def banChannel(self, request, channelId):
        try:
            channel = self.queryset.get(pk=channelId)
            channel.is_active = False
            channel.save()
            return Response({'Banned user successfully'}, status=status.HTTP_200_OK)
        except Channel.DoesNotExist:
            return Response({'message': 'Channel not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def unbanChannel(self, request, channelId):
        try:
            channel = self.queryset.get(pk=channelId)
            channel.is_active = True
            channel.save()
            return Response({'Banned user successfully'}, status=status.HTTP_200_OK)
        except Channel.DoesNotExist:
            return Response({'message': 'Channel not found'}, status=status.HTTP_404_NOT_FOUND)
            
@extend_schema(tags=['Member', 'Channel'])
class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    # Not necessary
    def deleteMember(self, request, memberId):
        try:
            member = self.queryset.get(pk=memberId)
            channel = Channel.objects.get(pk=member.channel.id)
            channel.save()
            member.delete()
            return Response({'message': 'Delete member successfully'})
        except Exception as e:
            return Response({'message': 'Member not found'}, status=status.HTTP_404_NOT_FOUND)
            
