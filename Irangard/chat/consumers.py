import json

from channels.exceptions import DenyConnection
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync
from accounts.models import User
from .models import Chat, Message, MessageRoom


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
    
    def disconnect(self, close_code):
        # Leave room
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
    
    # Receive message from web socket
    def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        room = data['room_name']
        sender_type = data['sender_type']
        
        user = User.objects.get(username=username)

        async_to_sync(self.save_message)(user, room, message, sender_type)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'sender_type':sender_type
            }
        )
    
    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        username = event['username']
        sender_type = event['sender_type']
        
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'sender_type':sender_type
        }))

    @sync_to_async
    def save_message(self, user, room, message, sender_type):
        Chat.objects.create(sender=user, room_name=room, message=message, sender_type=sender_type)


class MessageConsumer(WebsocketConsumer):
    def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        does_room_exists = MessageRoom.objects.filter(id=self.room_id).exists()
        self.room_group_name = 'chat_%s' % self.room_id
        if not does_room_exists:
            return DenyConnection
        # Join room
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from web socket
    def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        userid = data['userid']
        room_id = data['room']
        ''''
        {
            "message" : "from extetion",
            "userid" : "11",
            "room" : "2"
        }
        '''
        user = User.objects.get(id=userid)
        room = MessageRoom.objects.get(id=room_id)
        async_to_sync(self.save_message)(user, room, message)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'userid': userid
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        userid = event['userid']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'userid': userid,
        }))

    @sync_to_async
    def save_message(self, user, room, message):
        Message.objects.create(reciever_room=room, sender=user, message=message)