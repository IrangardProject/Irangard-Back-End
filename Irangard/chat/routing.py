from django.urls import path, re_path

from chat.consumers import ChatConsumer, MessageConsumer

websocket_urlpatterns = [
    re_path(r'chat/room/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
    re_path(r'ws/(?P<room_id>\w+)/$', MessageConsumer.as_asgi())
]