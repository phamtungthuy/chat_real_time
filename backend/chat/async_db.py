from message.models import Message, Reaction
from channel.models import Member, Channel
from user.models import UserProfile, Friend, Notification
from message.serializer import MessageSerializer, ReactionSerializer
from channel.serializer import MemberSerializer, ChannelSerializer
from user.serializer import NotificationSerializer
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
from rest_framework import serializers
from asgiref.sync import async_to_sync

    
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
    JOIN_CHANNEL = 'join_channel'
    CREATE_MESSAGE = 'create_message'
    REMOVE_MESSAGE = 'remove_message'
    CREATE_REACTION = 'create_reaction'
    REMOVE_REACTION = 'remove_reaction'
    ADD_MEMBER = 'add_member'
    REMOVE_MEMBER = 'remove_member'
    OUT_CHANNEL = 'out_channel'
    CHANGE_CREATOR = 'change_creator'
    DISBAND_CHANNEL = 'disband_channel'
    SET_CHANNEL_TITLE = 'set_channel_title'
    SET_NICKNAME = 'set_nickname'
    REMOVE_NICKNAME = 'remove_nickname'
    FRIEND_REQUEST = 'friend_request'
    FRIEND_ACCEPT = 'friend_accept'
    FRIEND_DENY = 'friend_deny'

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
def getUserChannels(user):
    members = user.members.all()
    channels = [member.channel for member in members]
    return channels

@database_sync_to_async
def isCreator(user, channelId):
    member = Member.objects.get(user=user, channel_id=channelId)
    if member.role == "CREATOR":
        return True
    return False

"""
text_json_data = {
    "action": "create_message",
    "target": "channel",
    "targetId": int,
    "data": {
        "content": str,
        "reply": int (null=True),
    }
}
"""
@database_sync_to_async
def createMessage(user, channelId, data):
    data['member'] = Member.objects.get(user=user, channel_id=channelId).id
    data['channel'] = channelId
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
        "message": int,
        "emoji": int
    }
}
"""
@database_sync_to_async
def createReaction(user, channelId, data):
    data['member'] = Member.objects.get(user=user, channel_id=channelId).id
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
    }
}
"""
@database_sync_to_async
def addMember(channelId, data):
    data['channel'] = channelId
    if (Member.objects.filter(user_id=data['user'], channel=channelId).exists()):
        raise Exception('This user has already been member')
    serializer = MemberSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return serializer.data

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
    "action": "out_channel",
    "target": "channel",
    "targetId": int,
    "data": {}
}
"""
@database_sync_to_async
def outChannel(user, channelId, data):
    member = Member.objects.get(user=user, channel_id=channelId)
    if member.role == 'CREATOR':
        raise Exception("You can not out channel while you are still creator")
    data['memberId'] = member.id
    member.delete()
    return data


"""
text_json_data = {
    "action": "change_creator",
    "target": "channel",
    "targetId": int,
    "data": {
        "memberId": int
    }
}
"""
@database_sync_to_async
def changeCreator(user, data):
    memberId = data.get('memberId')
    newCreator = Member.objects.get(pk=memberId)
    oldCreator = Member.objects.get(user=user, channel=newCreator.channel)
    oldCreator.role = "MEMBER"
    oldCreator.save()
    newCreator.role = "CREATOR"
    newCreator.save()
    return data


"""
text_json_data = {
    "action": "disband_channel",
    "target": "channel",
    "targetId": int,
    "data": {}
}
"""
@database_sync_to_async
def disbandChannel(channelId, data):
    channel = Channel.objects.get(pk=channelId)
    channel.delete()
    return data


"""
text_json_data = {
    "action": "set_channel_title",
    "target": "channel",
    "targetId": int,
    "data": {
        "title": str
    }
}
"""
@database_sync_to_async
def setChannelTitle(channelId, data):
    title = data.get('title')
    channel = Channel.objects.get(pk=channelId)
    serializer = ChannelSerializer(channel, data=data, partial=True)
    if serializer.is_valid(raise_exception=True):
        channel = serializer.update_title(title)
    data['title'] = channel.title
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
    serializer = MemberSerializer(member, data=data, partial=True)
    if (serializer.is_valid(raise_exception=True)):
        member = serializer.update_nickname(nickname)
    data['nickname'] = member.nickname
    return data


"""
text_json_data = {
    "action": "remove_nickname",
    "target": "channel",
    "targetId": int,
    "data": {
        "memberId": int,
    }
}
"""
@database_sync_to_async
def removeNickname(data):
    memberId = data.get('memberId')
    member = Member.objects.get(pk=memberId)
    member.nickname = None
    member.save()
    return data


"""
text_json_data = {
    "action": "friend_request",
    "target": "user",
    "targetId": int,
    "data": {}
}
"""
@database_sync_to_async
def friendRequest(user, receiver, data):
    data.update({
        "receiver": receiver,
        "sender": user.id,
        "notification_type": "FRIEND_REQUEST"
    })
    if Notification.objects.filter(
        receiver_id=data['receiver'],
        sender_id=data['sender'],
        notification_type="FRIEND_REQUEST",
        status="PENDING"
    ).exists():
        raise Exception("You have already sent friend request to this user")
    serializers = NotificationSerializer(data=data)
    if (serializers.is_valid(raise_exception=True)):
        serializers.save()
        return serializers.data


"""
text_json_data = {
    "action": "friend_accept",
    "target": "user",
    "targetId": int,
    "data": {}
}
"""
@database_sync_to_async
def friendAccept(consumer, receiver, data):
    user = consumer.user
    friend_with = User.objects.get(pk=receiver)
    if Friend.objects.filter(user=user, friend_with=friend_with).exists() \
    or Friend.objects.filter(user=friend_with, friend_with=user).exists():
        raise Exception("You have already been friend")
    
    Friend.objects.create(user=user, friend_with=friend_with)
    Friend.objects.create(user=friend_with, friend_with=user)

    for channel in Channel.objects.all():
        members = channel.members.all()
        if members.count() == 2:
            if ((members[0].user == user and members[1].user.id == receiver)
            or (members[1].user == user and members[0].user.id == receiver)):
                if not channel.is_active:
                    channel.is_active = True
                    channel.save()
                    data.update({
                        "receiver": receiver,
                        "sender": user.id,
                        "notification_type": "FRIEND_ACCEPT",
                        "status": "HANDLED"
                    })
                    serializer = NotificationSerializer(data=data)
                    if (serializer.is_valid(raise_exception=True)):
                        serializer.save()
                        return serializer.data

    channel = Channel.objects.create(
        title=f'{user.username} || {friend_with.username}',
        avatar_url=user.profile.avatar_url
    )
    Member.objects.create(user=user, channel=channel)
    Member.objects.create(user=friend_with, channel=channel)
    
    requestToAccept = Notification.objects.filter(sender_id=receiver,
        receiver=user,
        notification_type='friend_request',
        status='pending'
    ).first()
    if requestToAccept:
        requestToAccept.status = 'HANDLED'
        requestToAccept.save()

    async_to_sync(consumer.joinChannel)()
    data.update({
        "receiver": receiver,
        "sender": user.id,
        "notification_type": "FRIEND_ACCEPT",
        "status": "HANDLED"
    })
    serializer = NotificationSerializer(data=data)
    if (serializer.is_valid(raise_exception=True)):
        serializer.save()
        return serializer.data

"""
text_json_data = {
    "action": "friend_deny",
    "target": "user",
    "targetId": userId
}
"""

@database_sync_to_async
def friendDeny(receiver, senderId):
    requestToDeny = Notification.objects.filter(
        receiver=receiver,
        sender_id=senderId,
        status='pending',
        notification_type="friend_request"
    ).first()
    if requestToDeny:
        requestToDeny.status = 'HANDLED'
        requestToDeny.save()
        serializer = NotificationSerializer(requestToDeny)
        return serializer.data
    else:
        raise Exception("You don't have friend request to deny")