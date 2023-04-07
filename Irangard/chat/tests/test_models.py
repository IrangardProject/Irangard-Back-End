from email.mime import image
from django.test import TestCase
from ..models import Chat
from accounts.models import User
from rest_framework.test import APIClient
import io
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
import json
from rest_framework import status


class ChatTestCase(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.user = self.make_user(username='test human', password='123456', email='test@gmail.com')
        token = self.login(self.user.username, self.user.password)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        Chat.objects.create(sender=self.user, message='This is a text', 
                            room_name='room', sender_type='SERVER')
        
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
    

    def test_message(self):
        chat = Chat.objects.get(message="This is a text")
        self.assertEqual(chat.message, "This is a text")
        
    
    def test_room(self):
        chat = Chat.objects.get(room_name="room")
        self.assertEqual(chat.room_name, "room")
        
    def test_sender_type(self):
        chat = Chat.objects.get(message="This is a text")
        self.assertEqual(chat.sender_type, "SERVER")
