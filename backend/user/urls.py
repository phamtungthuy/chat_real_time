from django.urls import path
from .views import UserViewSet, FriendViewSet

urlpatterns = [
    path('', UserViewSet.as_view({
        'post': 'create',
    })),
    path('verify/', UserViewSet.as_view({
        'post': 'verifyEmail',
    })),
    path('channels/', UserViewSet.as_view({
        'get': 'getChannelList',
    })),
    path('upload/avatar/', UserViewSet.as_view({
        'post': 'uploadUserAvatar',
    })),
    # path('<int:id>/user/', UserViewSet.as_view({
    #     'get': 'retrieve',
    #     'put': 'update',
    #     'delete': 'delete'
    # })),
    path('user/<str:username>/', UserViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'delete'
    })),
    # FriendViewSet
    path('friends/', FriendViewSet.as_view({
        'get': 'getFriendList',
    })),
    path('friend/<int:friendId>/', FriendViewSet.as_view({
        'delete': 'deleteFriend',
    }))
]