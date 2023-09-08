from message.models import Message, Reaction
from message.serializer import MessageSerializer, ReactionSerializer
from channels.db import database_sync_to_async
    
class DATA_TYPE:
    MESSAGE = 'message'
    REACTION = 'reaction'

class ACTION:
    CREATE = 'create'
    UPDATE = 'update'
    DELETE = 'delete'


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
    return messageId


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
    return reactionId