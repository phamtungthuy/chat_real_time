from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

def index(request):
    return render(request, "chat/index.html")

def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})

def call(request):
    return render(request, 'chat/call.html')