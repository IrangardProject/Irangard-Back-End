from django.test import TestCase
from ..models import Chat, MessageRoom, UserInRoom, Message
from accounts.models import User
from rest_framework.test import APIClient
from django.urls import reverse
import json
from rest_framework import status

OKGREEN = '\033[92m'
ENDC = '\033[0m'

class MessageModelTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = self.make_user(username='test human', password='123456', email='test@gmail.com')
        token = self.login(self.user.username, self.user.password)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

    def login(self, username, password):
        url = reverse('accounts:accounts-jwt-create')
        data = json.dumps({'username': username, 'password': password})
        response = self.client.post(url, data, content_type='application/json')
        if response.status_code == status.HTTP_200_OK:
            access_token = response.data['access']
            return access_token
        else:
            return "incorrect"

    def make_user(self, username, password, email):
        self.user = User.objects.create(username=username, email=email)
        self.user.set_password(password)
        self.user.save()
        return self.user

    def test_message_room(self):
        room = MessageRoom.objects.create(name='room_name', owner=self.user)
        self.assertEqual(room.name, 'room_name')
        self.assertEqual(room.owner, self.user)
        print(f"{OKGREEN}Message Room model test passed successfully{ENDC}")
        return True

    def test_user_in_room(self):
        new_room = MessageRoom.objects.create(name='room_name', owner=self.user)
        user_in_room_obj = UserInRoom.objects.create(user=self.user, room=new_room)
        self.assertEqual(user_in_room_obj.user, self.user)
        self.assertEqual(user_in_room_obj.room, new_room)
        print(f"{OKGREEN}UserInRoom model test passed successfully{ENDC}")
        return True

    def test_message(self):
        receiver_room = MessageRoom.objects.create(name='room_name', owner=self.user)
        message_body = 'Hello this is a test message'
        message = Message.objects.create(reciever_room=receiver_room, sender=self.user, message=message_body)
        self.assertEqual(message.message, message_body)
        self.assertEqual(message.sender, self.user)
        self.assertEqual(message.reciever_room, receiver_room)
        print(f"{OKGREEN}Message model test passed successfully{ENDC}")
        return True
