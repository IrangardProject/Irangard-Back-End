from django.urls import path

from chat.consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/room/', ChatConsumer.as_asgi()),
]