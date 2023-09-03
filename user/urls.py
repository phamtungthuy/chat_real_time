from django.urls import path
from .views import UserViewSet

urlpatterns = [
    path('user/', UserViewSet.as_view({
        'post': 'create',

    })),
    path('<int:id>/user/', UserViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'delete'
    })),
    path('user/<str:username>', UserViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'delete'
    }))
]