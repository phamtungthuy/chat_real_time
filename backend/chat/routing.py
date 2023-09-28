from django.urls import path
from .consumers import LobbyConsumer, ChatConsumer

websocket_urlpatterns = [
    path('ws/lobby/', LobbyConsumer.as_asgi()),
    path('ws/chat/<str:chatRoomId>/', ChatConsumer.as_asgi()),
]