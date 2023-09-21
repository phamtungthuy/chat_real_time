from django.urls import path
from .views import ChannelViewSet, MemberViewSet

urlpatterns = [
    path('channel/', ChannelViewSet.as_view({
        'post': 'createChannel',
    })),
    path('channel/<int:channelId>/', ChannelViewSet.as_view({
        'delete': 'deleteChannel',
    })),
    path('channel/<int:channelId>/members', ChannelViewSet.as_view({
        'get': 'getMemberList',
    }))
]
