from django.urls import path
from .views import MessageViewSet, ReactionViewSet, getEmojiList

urlpatterns = [
    # Message url
    path('upload/image/', MessageViewSet.as_view({
        'post': 'uploadImage',
    })),
    path('<int:messageId>/', MessageViewSet.as_view({
        'put': 'editMessage',
        'delete': 'deleteMessage',
    })),

    # Reaction url
    path('<int:messageId>/reactions/', ReactionViewSet.as_view({
        'get': 'getReactionList',
    })),
    # path('reaction/', ReactionViewSet.as_view({
    #    'post': 'createReaction',
    # })),
    # path('reaction/<int:reactionId>/', ReactionViewSet.as_view({
    #     'put': 'changeReaction',
    #     'delete': 'removeReaction',
    # })),

    # Emoji url
    path('emojis/', getEmojiList),
]