from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from django.db.models import F, Value, CharField, Q
from django.db.models.functions import Concat
from rest_framework import status
from django.contrib.auth.models import User
from channel.models import Channel, Member
from .serializer import SearchChannelSerializer, SearchUserSerializer, SearchMessageSerializer
from .schema import searchChannelSchema, searchFriendSchema, searchMessageSchema

@searchChannelSchema
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def searchChannel(request):
    query = request.GET.get('query', '')

    # Get user's channel
    user = request.user
    members = user.members.all()
    userChannel = Channel.objects.filter(members__user=user).distinct()
    
    # Search in channel
    channelResult = userChannel.filter(title__icontains=query)
    
    # Search in user
    userResult = User.objects.annotate(
        fullname=Concat(F('first_name'), Value(' '), F('last_name'), output_field=CharField())
    ).filter(Q(fullname__icontains=query) | Q(username__icontains=query))

    channelSerializer = SearchChannelSerializer(channelResult, many=True)
    userSerializer = SearchUserSerializer(userResult, many=True)
    return Response({"users": userSerializer.data,
                    "channels": channelSerializer.data,
                    "resultSize": userResult.count() + channelResult.count()})


@searchMessageSchema
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def searchMessage(request, channelId):
    query = request.GET.get('query', '')
    user = request.user
    try:
        channel = Channel.objects.get(pk=channelId)
        if not channel.members.filter(user=user):
            return Response({"message": "You are not member of this channel"}, status.HTTP_403_FORBIDDEN)
        messages = channel.messages.filter(message_type="text")
        messageResult = messages.filter(content__icontains=query)
        messageSerializer = SearchMessageSerializer(messageResult, many=True)
        return Response({"messages": messageSerializer.data, "resultSize": messageResult.count()})
    except:
        return Response({"message": "Channel not found"}, status=status.HTTP_404_NOT_FOUND)


@searchFriendSchema
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def searchFriend(request):
    user = request.user
    query = request.GET.get('query', '')
    friends = user.friends

    friendResult = friends.annotate(
        fullname=Concat(F('friend_with__first_name'), Value(' '), F('friend_with__last_name'), output_field=CharField()),
        username=F('friend_with__username')
    ).filter(Q(fullname__icontains=query) | Q(username__icontains=query))
    
    userResult = [friend.friend_with for friend in friendResult]
    friendSerializer = SearchUserSerializer(userResult, many=True)
    return Response({"friends": friendSerializer.data, "resultSize": friendResult.count()})