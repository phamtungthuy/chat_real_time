from django.urls import path
from . import views

urlpatterns = [
    path('channel/', views.searchChannel),
    path('channel/<int:channelId>/message/', views.searchMessage),
    path('friend/', views.searchFriend),
]