from django.test import TestCase
from ..models import Chat
from accounts.models import User
from rest_framework.test import APIClient
from django.urls import reverse
import json
from rest_framework import status


class ChatTestCase(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.url = 'http://127.0.0.1:8000/chat/'
        self.user = self.make_user(username='test human', password='123456', email='test@gmail.com')
        token = self.login(self.user.username, self.user.password)
        # self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        self.chat = Chat.objects.create(sender=self.user, message='This is a text', 
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


    def test_get_chats(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    

    def test_post_chat(self):
        data = {
            "sender": self.user.pk,
            "message": 'this is a new message',
            "room_name": self.chat.room_name,
            "sender_type": "SERVER"
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_retrieve_room_chats(self):
        url = self.url + 'room/messages/{}/'.format(self.chat.room_name)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_retrieve_chat(self):
        url = self.url + '{}/'.format(self.chat.pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    def test_put_chat(self):
        url = self.url + '{}/'.format(self.chat.pk)
        data = {
            "sender": self.user.pk,
            "message": "I put a new message! and changed it",
            "room_name": self.chat.room_name,
            "sender_type": "SERVER"
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_patch_chat(self):
        url = self.url + '{}/'.format(self.chat.pk)
        data = {
            "message": "I put a new message! and changed it",
        }
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    def test_delete_chat(self):
        url = self.url + '{}/'.format(self.chat.pk)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)