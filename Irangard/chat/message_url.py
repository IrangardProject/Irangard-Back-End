from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import *
from . import views




message_router = routers.DefaultRouter()
message_router.register('', MessageViewSet, basename='message')

room_router = routers.DefaultRouter()
room_router.register('', MessageRoomViewSet, basename='room')

urlpatterns = [
    path('room/chats/<int:pk>', RoomAllMessages.as_view(), name='room-chats'),
    path('room/', include(room_router.urls), name='room'),
    path('', include(message_router.urls), name='message'),
]
