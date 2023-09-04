from django.urls import path
from .views import MessageViewSet

urlpatterns = [
    path('all/<int:channelId>/', MessageViewSet.as_view({
        'get': 'getMessageList'
    })),
    path('', MessageViewSet.as_view({
        'post': 'createMessage',
    })),
    path('<int:messageId>/', MessageViewSet.as_view({
        'put': 'editMessage',
        'delete': 'deleteMessage',
    })),
]