from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema
from .models import Channel, Member
from .serializer import ChannelSerializer,MemberSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User


class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ChannelSerializer

    def createChannel(self, request):
        data = request.data
        title = data.get('title')
        creator = data.get('creator')
        members = data.get('members')
        memberCount = len(members)
        try:
            channel = self.queryset.create(title=title, memberCount=memberCount)
            Member.objects.create(user_id=creator, channel=channel, role="CREATOR")
            for user in members:
                Member.objects.create(user_id=user, channel=channel, role="MEMBER")
            serializer = self.serializer_class(channel, many=False)
            return Response({'message': 'Create channel successfully', 'data': serializer.data})
        except Exception as e:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        

    def getMemberList(self, request, channelId):
        try:
            channel = self.queryset.get(pk=channelId)
            memberList = channel.members.all()
            print(memberList)
            serializer = MemberSerializer(memberList, many=True)
            return Response({'message': 'Get member list successfully', 'data': serializer.data})
        except Exception as e:
            return Response({'message': 'Channel not found'}, status=status.HTTP_404_NOT_FOUND)
            

    def deleteChannel(self, request, channelId):
        try:
            channel = self.queryset.get(pk=channelId)
            channel.delete()
            return Response({'message': 'Delete channel successfully'})
        except Exception as e:
            return Response({'message': 'Channel not found'}, status=status.HTTP_404_NOT_FOUND)
            

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    permission_classes = [AllowAny]
    serializer_class = MemberSerializer

    def deleteMember(self, request, memberId):
        try:
            member = self.queryset.get(pk=memberId)
            channel = Channel.objects.get(pk=member.channel.id)
            channel.memberCount = channel.memberCount - 1
            channel.save()
            member.delete()
            return Response({'message': 'Delete member successfully'})
        except Exception as e:
            return Response({'message': 'Member not found'}, status=status.HTTP_404_NOT_FOUND)
            
