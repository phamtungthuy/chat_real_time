from django.urls import path
from .views import ChannelViewSet, MemberViewSet

urlpatterns = [
    path('', ChannelViewSet.as_view({
        'post': 'createChannel',
    })),
    path('<int:channelId>/', ChannelViewSet.as_view({
        'delete': 'deleteChannel',
    })),
    path('all/', ChannelViewSet.as_view({
        'get': 'getAllChannels',
    })),
    path('upload/avatar/', ChannelViewSet.as_view({
        'post': 'uploadChannelAvatar',
    })),
    path('<int:channelId>/members/', ChannelViewSet.as_view({
        'get': 'getMemberList',
    })),
    path('<int:channelId>/messages/', ChannelViewSet.as_view({
        'get': 'getMessageList',
    })),
    path('<int:channelId>/media/', ChannelViewSet.as_view({
        'get': 'getMediaList',
    })),
    # MemberViewSet
    path('member/<int:memberId>/', MemberViewSet.as_view({
        'delete': 'deleteMember',
    })),
    path('ban/<int:channelId>/', ChannelViewSet.as_view({
        'post': 'banChannel',
    })),
    path('unban/<int:channelId>/', ChannelViewSet.as_view({
        'post': 'unbanChannel',
    })),
]
