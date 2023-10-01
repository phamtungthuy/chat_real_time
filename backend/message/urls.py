from django.urls import path
from .views import MessageViewSet, ReactionViewSet, getEmojiList

urlpatterns = [
    # Message url
    path('all/<int:channelId>/', MessageViewSet.as_view({
        'get': 'getMessageList',
    })),
    path('upload/', MessageViewSet.as_view({
        'post': 'uploadImageMessage',
    })),
    path('<int:messageId>/', MessageViewSet.as_view({
        'put': 'editMessage',
        'delete': 'deleteMessage',
    })),

    # Reaction url
    path('reaction/all/<int:messageId>/', ReactionViewSet.as_view({
        'get': 'getReactionList',
    })),
    path('reaction/', ReactionViewSet.as_view({
       'post': 'createReaction',
    })),
    path('reaction/<int:reactionId>/', ReactionViewSet.as_view({
        'put': 'changeReaction',
        'delete': 'removeReaction',
    })),

    # Emoji url
    path('emoji/all/', getEmojiList),
]