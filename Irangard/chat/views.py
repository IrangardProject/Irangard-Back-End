from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .models import Chat
from .serializers import ChatSerializer


class ChatViewSet(ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    # permission_classes = IsAuthenticated

    @action(
        detail=False,
        methods=['get', 'post'],
        url_path=r'index',
        url_name='chat_index',
        permission_classes=[AllowAny]
    )
    def index(self, request):

        return render(request, 'chat/index.html')

    @action(
        detail=True,
        methods=['get', 'post'],
        url_path=r'room/(?P<room_name>\w+)/username/(?P<username>\w+)',
        url_name='chat_room',
        permission_classes=[AllowAny]
    )
    def room(self, request, room_name, username):

        # messages = Message.objects.filter(room=room_name)[0:25]

        return render(request, 'chat/room.html', {'room_name': room_name, 'username': username, 'messages': messages})


def room(request, room_name, username):
    messages = Chat.objects.filter(room_name=room_name)[0:25]
    return render(request, 'chat/room.html', {'room_name': room_name, 'username': username, 'messages': messages})