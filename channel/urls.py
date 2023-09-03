from django.urls import path
from channel import views

urlpatterns = [
    path('create/', views.createChannel),
    path('getAll/', views.getAllChannels),
    path('update/', views.updateChannel),
    path('delete/<int:channelId>', views.deleteChannel)
]
