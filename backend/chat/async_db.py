from message.models import Message, Reaction
from message.serializer import MessageSerializer, ReactionSerializer
from channel.serializer import MemberSerializer
from channel.models import Member
from channels.db import database_sync_to_async
    

class ACTION:
    CREATE_MESSAGE = 'create_message'
    DELETE_MESSAGE = 'delete_message'
    CREATE_REACTION = 'create_reaction'
    DELETE_REACTION = 'delete_reaction'
    ADD_MEMBER = 'add_member'
    REMOVE_MEMBER = 'remove_member'
    UPDATE_CHANNEL = 'update_channel'


@database_sync_to_async
def createMessage(data):
    serializer = MessageSerializer(data=data)
    if (serializer.is_valid(raise_exception=True)):
        serializer.save()
        return serializer.data


@database_sync_to_async
def deleteMessage(data):
    messageId = data.get('messageId')
    message = Message.objects.get(pk=messageId)
    message.delete()
    return {'messageId': messageId}


@database_sync_to_async
def createReaction(data):
    serializer = ReactionSerializer(data=data)
    if (serializer.is_valid(raise_exception=True)):
        serializer.save()
        return serializer.data


@database_sync_to_async
def deleteReaction(data):
    reactionId = data.get('reactionId')
    reaction = Reaction.objects.get(pk=reactionId)
    reaction.delete()
    return {'reactionId': reactionId}


@database_sync_to_async
def addMember(data):
    serializer = MemberSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return serialzier.data


@database_sync_to_async
def removeMember(data):
    memberId = data.get('memberId')
    member = Member.objects.get(pk=memberId)
    member.delete()
    return {'memberId': memberId}


@database_sync_to_async
def updateChannel(data):
    serializer = MemberSerializer(instance=instance, data=data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return serialzier.data