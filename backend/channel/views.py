from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema
from .models import Channel, Member
from .serializer import ChannelSerializer,MemberSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny


class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ChannelSerializer

    def createChannel(request):
        data = request.data
        title = data.get('title')
        members = data.get('members')
        memberCount = members.len
        try:
            for user in members:
                Member.objects.create(user=user, channel=channel, role="MEMBER")
            channel = self.queryset.create(title=title, memberCount=memberCount)
            serializer = serializer_class(channel, many=False)
            return Response({message: 'Create channel successfully', data: serializer.data})
        except User.DoesNotExist:
            return Response({message: 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        

    def getMemberList(request, channelId):
        try:
            channel = self.queryset.get(pk=channelId)
            memberList = channel.members
            serializer = serializer_class(memberList, many=True)
            return serializer({message: 'Get member list successfully', data: serializer.data})
        except:
            return Response({message: 'Channel not found'}, status=status.HTTP_404_NOT_FOUND)
            

    def deleteChannel(request, channelId):
        try:
            channel = queryset.get(pk=channelId)
            channel.delete()
            return Response({message: 'Delete channel successfully'})
        except:
            return Response({message: 'Channel not found'}, status=status.HTTP_404_NOT_FOUND)
            

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    permission_classes = [AllowAny]
    serializer_class = MemberSerializer

    def deleteMember(request, memberId):
        try:
            member = self.queryset.get(pk=memberId)
            member.delete()
            return Response({message: 'Delete member successfully'})
        except:
            return Response({message: 'Member not found'}, status=status.HTTP_404_NOT_FOUND)
            
