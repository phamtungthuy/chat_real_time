from django.urls import path
from message import views

urlpatterns = [
    path('create/', views.createMessage),
    path('getAll/', views.getAllMessages),
    path('delete/<int:messageId>', views.deleteMessage)
]