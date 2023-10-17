from django.urls import path
from .views import UserViewSet, UserProfileViewSet, FriendViewSet, NotificationViewSet

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
    path('all/', UserViewSet.as_view({
        'get': 'getAllUsers',
    })),
    # path('<int:userId>/', UserViewSet.as_view({
    #     'get': 'retrieve',
    #     'put': 'update',
    #     'delete': 'deleteUser'
    # })),    
    # path('<int:id>/user/', UserViewSet.as_view({
    #     'get': 'retrieve',
    #     'put': 'update',
    #     'delete': 'delete'
    # })),
    
    # UserProflieViewSet
    path('profile/', UserProfileViewSet.as_view({
        'put': 'updateUserProfile',
    })),
    path('profile/avatar/', UserProfileViewSet.as_view({
        'put': 'uploadUserAvatar',
    })),
    path('<int:userId>/profile', UserProfileViewSet.as_view({
        'get': 'getUserProfile',
    })),

    # FriendViewSet
    path('friends/', FriendViewSet.as_view({
        'get': 'getFriendList',
    })),
    path('friend/<int:friendId>/', FriendViewSet.as_view({
        'delete': 'deleteFriend',
    })),

    # NotificationViewSet
    path('notifications/', NotificationViewSet.as_view({
        'get': 'getNotificationList'
    }))
]