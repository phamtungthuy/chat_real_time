from django.urls import path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/chat/<int:groupId>/', ChatConsumer.as_asgi()),
]