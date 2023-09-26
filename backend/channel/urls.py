from django.urls import path
from .views import ChannelViewSet, MemberViewSet

urlpatterns = [
    path('', ChannelViewSet.as_view({
        'post': 'createChannel',
    })),
    path('<int:channelId>/', ChannelViewSet.as_view({
        'delete': 'deleteChannel',
    })),
    path('<int:channelId>/members', ChannelViewSet.as_view({
        'get': 'getMemberList',
    })),
    path('member/<int:memberId>/', MemberViewSet.as_view({
        'delete': 'deleteMember',
    }))
]
