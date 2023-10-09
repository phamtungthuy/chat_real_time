from django.urls import path
from .views import UserViewSet, UserProfileViewSet, FriendViewSet

urlpatterns = [
    path('signup/', UserViewSet.as_view({
        'post': 'signup',
    })),
    path('login/', UserViewSet.as_view({
        'post': 'login',
    })),
    path('verify/', UserViewSet.as_view({
        'post': 'verifyEmail',
    })),
    path('verify/resend/', UserViewSet.as_view({
        'post': 'resendVerification',
    })),
    path('channels/', UserViewSet.as_view({
        'get': 'getChannelList',
    })),
    path('upload/avatar/', UserViewSet.as_view({
        'post': 'uploadUserAvatar',
    })),
    path('user/<str:username>/', UserViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'deleteUser'
    })),
    # Admin request
    path('all/', UserViewSet.as_view({
        'get': 'getAllUsers',
    })),
    # path('<int:id>/user/', UserViewSet.as_view({
    #     'get': 'retrieve',
    #     'put': 'update',
    #     'delete': 'delete'
    # })),
    
    # UserProflieViewSet
    path('profile/<int:userId>/', UserProfileViewSet.as_view({
        'get': 'getUserProfile',
    })),

    # FriendViewSet
    path('friends/', FriendViewSet.as_view({
        'get': 'getFriendList',
    })),
    path('friend/<int:friendId>/', FriendViewSet.as_view({
        'delete': 'deleteFriend',
    }))
]