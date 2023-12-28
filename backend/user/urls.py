from django.urls import path
from .views import UserViewSet, UserProfileViewSet, FriendViewSet, NotificationViewSet
from .providerAuth import facebookAuthURL, facebookAuth, googleAuthURL, googleAuth
from .passwordToken import *

urlpatterns = [
    # Authentication
    path('auth/facebook/', facebookAuthURL),
    path('auth/facebook/callback/', facebookAuth),
    path('auth/google/', googleAuthURL),
    path('auth/google/callback/', googleAuth),


    path('', UserViewSet.as_view({
        'get': 'retrieveUser'
    })),
    path('signup/', UserViewSet.as_view({
        'post': 'signup',
    })),
    path('login/', UserViewSet.as_view({
        'post': 'login',
    })),
    path('verify-user/', UserViewSet.as_view({
        'post': 'verifyEmail',
    })),
    path('verify-user/resend/', UserViewSet.as_view({
        'post': 'resendVerification',
    })),
    path('change-password/', UserViewSet.as_view({
        'put': 'changePassword'
    })),
    path('change-email/', UserViewSet.as_view({
        'put': 'changeEmail'
    })),
    path('verify-email/', UserViewSet.as_view({
        'post': 'verifyChangeEmail'
    })),
    path('ban/<int:userId>/', UserViewSet.as_view({
        'post': 'banUser'
    })),
    path('unban/<int:userId>/', UserViewSet.as_view({
        'post': 'unbanUser'
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
        'get': 'getSelfProfile',
        'put': 'updateUserProfile',
    })),
        path('<int:userId>/profile', UserProfileViewSet.as_view({
        'get': 'getUserProfile',
    })),
    path('profile/avatar/', UserProfileViewSet.as_view({
        'put': 'uploadUserAvatar',
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
    })),
    path('sent-notifications/', NotificationViewSet.as_view({
        'get': 'getSentFriendRequestList'
    })),


    path('passwordreset/', 
         CustomResetPasswordRequestTokenViewSet.as_view({
            'post': 'create'     
        })),
    path('passwordreset/confirm/', 
         CustomResetPasswordConfirmViewSet.as_view({
            'post': 'create'     
        })),
    path('passwordreset/validate/', 
         CustomResetPasswordValidateTokenViewSet.as_view({
            'post': 'create'     
        }))
]