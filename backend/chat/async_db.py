from message.models import Message, Reaction
from channel.models import Member, Channel
from user.models import UserProfile, Friend, Notification
from message.serializer import MessageSerializer, ReactionSerializer
from channel.serializer import MemberSerializer, ChannelSerializer
from user.serializer import NotificationSerializer
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
from rest_framework import serializers
    
# text_json_data = {
#     "action": ACTION,
#     "target": TARGET,
#     "data": {
#         "member": member,
#         "channel": channel,
#         ...
#     }
# }

class ACTION:
    CREATE_MESSAGE = 'create_message'
    REMOVE_MESSAGE = 'remove_message'
    CREATE_REACTION = 'create_reaction'
    REMOVE_REACTION = 'remove_reaction'
    ADD_MEMBER = 'add_member'
    REMOVE_MEMBER = 'remove_member'
    SET_CHANNEL_TITLE = 'set_channel_title'
    SET_NICKNAME = 'set_nickname'
    FRIEND_REQUEST = 'friend_request'
    FRIEND_ACCEPT = 'friend_accept'

class TARGET:
    USER = 'user'
    CHANNEL = 'channel'

@database_sync_to_async
def setOnlineUser(user):
    userProfile = UserProfile.objects.get(user=user)
    userProfile.online = True
    userProfile.save()

@database_sync_to_async
def setOfflineUser(user):
    userProfile = UserProfile.objects.get(user=user)
    userProfile.online = False
    userProfile.save()

@database_sync_to_async
def getOnlineUser():
    onlineUser = UserProfile.objects.filter(online=True)
    return onlineUser

@database_sync_to_async
def getUserChannels(user):
    members = user.members.all()
    channels = [member.channel for member in members]
    return channels

"""
text_json_data = {
    "action": "create_message",
    "target": "channel",
    "targetId": int,
    "data": {
        "member": int,
        "channel": int,
        "content": str,
        "reply": int (null=True),
    }
}
"""
@database_sync_to_async
def createMessage(data):
    serializer = MessageSerializer(data=data)
    if (serializer.is_valid(raise_exception=True)):
        serializer.save()
        return serializer.data

"""
text_json_data = {
    "action": "remove_message",
    "target": "channel",
    "targetId": int,
    "data": {
        "messageId": int
    }
}
"""
@database_sync_to_async
def removeMessage(data):
    messageId = data.get('messageId')
    message = Message.objects.get(pk=messageId)
    message.delete()
    return data

"""
text_json_data = {
    "action": "create_reaction",
    "target": "channel",
    "targetId": int,
    "data": {
        "member": int,
        "message": int,
        "emoji": int
    }
}
"""
@database_sync_to_async
def createReaction(data):
    serializer = ReactionSerializer(data=data)
    if (serializer.is_valid(raise_exception=True)):
        serializer.save()
        return serializer.data

"""
text_json_data = {
    "action": "remove_reaction",
    "target": "channel",
    "targetId": int,
    "data": {
        "reactionId": int
    }
}
"""
@database_sync_to_async
def removeReaction(data):
    reactionId = data.get('reactionId')
    reaction = Reaction.objects.get(pk=reactionId)
    reaction.delete()
    return data

"""
text_json_data = {
    "action": "add_member",
    "target": "channel",
    "targetId": int,
    "data": {
        "user": int,
        "channel": int,
    }
}
"""
@database_sync_to_async
def addMember(data):
    serializer = MemberSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return serialzier.data

"""
text_json_data = {
    "action": "remove_member",
    "target": "channel",
    "targetId": int,
    "data": {
        "memberId": int
    }
}
"""
@database_sync_to_async
def removeMember(data):
    memberId = data.get('memberId')
    member = Member.objects.get(pk=memberId)
    member.delete()
    return data


"""
text_json_data = {
    "action": "set_channel_title",
    "target": "channel",
    "targetId": int,
    "data": {
        "channelId": int,
        "title": str
    }
}
"""
@database_sync_to_async
def setChannelTitle(data):
    channelId = data.get('channelId')
    title = data.get('title')
    title = title.strip()
    if title == "":
        serializers.ValidationError('Title must not be blank')
    channel = Channel.objects.get(pk=channelId)
    channel.title = title
    channel.save()
    data['title'] = title
    return data

"""
text_json_data = {
    "action": "set_nickname",
    "target": "channel",
    "targetId": int,
    "data": {
        "memberId": int,
        "nickname": str
    }
}
"""
@database_sync_to_async
def setNickname(data):
    memberId = data.get('memberId')
    nickname = data.get('nickname')
    member = Member.objects.get(pk=memberId)
    nickname = nickname.strip()
    if nickname == "":
        raise serializers.ValidationError('Nickname must not be blank')
    member.nickname = nickname
    member.save()
    data['nickname'] = member.nickname
    return data

"""
text_json_data = {
    "action": "friend_request",
    "target": "user",
    "targetId": int,
    "data": {
        "receiver": int
    }
}
"""
@database_sync_to_async
def friendRequest(user, data):
    data.update({
        "sender": user.id,
        "notification_type": "FRIEND_REQUEST"
    })
    serializers = NotificationSerializer(data=data)
    if (serializers.is_valid(raise_exception=True)):
        serializers.save()
        return serializers.data

"""
text_json_data = {
    "action": "friend_request",
    "target": "user",
    "targetId": int,
    "data": {
        "receiver": int,
    }
}
"""
@database_sync_to_async
def friendAccept(user, data):
    friend_with = data.get('user')
    Friend.objects.create(user=user, friend_with_id=friend_with)
    data.update({
        "sender": user.id,
        "notification_type": "FRIEND_ACCEPT"
    })
    serializer = NotificationSerializer(data=data)
    if (serializer.is_valid(raise_exception=True)):
        serializer.save()
        return serializer.data