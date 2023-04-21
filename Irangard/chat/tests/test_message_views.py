from django.test import TestCase
from ..models import Chat, MessageRoom, UserInRoom, Message
from accounts.models import User
from rest_framework.test import APIClient
from django.urls import reverse
import json
from rest_framework import status

OKGREEN = '\033[92m'
ENDC = '\033[0m'

class MessageViewTestCase(TestCase):

    def setUp(self):
        self.client_user_one = APIClient()
        self.client_user_two = APIClient()
        self.user_one = self.make_user(username='user_one', password='123456', email='user_one@gmail.com')
        self.user_two = self.make_user(username='user_two', password='123456', email='user_two@gmail.com')
        token_for_user_one = self.login(self.user_one.username, '123456', self.client_user_one)
        token_for_user_two = self.login(self.user_two.username, '123456', self.client_user_two)
        self.client_user_one.credentials(HTTP_AUTHORIZATION='JWT ' + token_for_user_one)
        self.client_user_two.credentials(HTTP_AUTHORIZATION='JWT ' + token_for_user_two)
        self.room_viewSet_url = 'http://localhost:8000/message/room/'
        self.message_viewSet_url = 'http://localhost:8000/message/'
        # self.room_all_messages_url = 'room/chats/<int:pk>'


    def login(self, username, password, client):
        url = reverse('accounts:accounts-jwt-create')
        data = json.dumps({'username': username, 'password': password})
        response = client.post(url, data, content_type='application/json')
        if response.status_code == status.HTTP_200_OK:
            access_token = response.data['access']
            return access_token
        else:
            return "incorrect"

    def make_user(self, username, password, email):
        user = User.objects.create(username=username, email=email)
        user.set_password(password)
        user.save()
        return user


    def test_new_message_room(self):
        data = {
            'name': 'test_room',
            'owner': self.user_one
        }
        response = self.client_user_one.post(self.room_viewSet_url, data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        new_room_id = response.data['id']
        self.assertEqual(MessageRoom.objects.filter(id=new_room_id).count(), 1)
        list_of_rooms = self.client_user_one.get(self.room_viewSet_url)
        self.assertEquals(list_of_rooms.status_code, status.HTTP_200_OK)
        self.assertEquals(len(list_of_rooms.data), 1)
        self.assertEquals(list_of_rooms.data[0].get('id'), new_room_id)
        print(f"{OKGREEN}Room creation test passed !{ENDC}")

    def test_message_room_retrieve(self):
        new_room = MessageRoom.objects.create(name='test_room', owner=self.user_one)
        new_room.save()
        response = self.client_user_one.get(f"{self.room_viewSet_url}{new_room.id}/")
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        new_room_id = response.data['id']
        self.assertEquals(response.data['name'], new_room.name)
        print(f"{OKGREEN}Room retrieve test passed !{ENDC}")

    def test_add_user_in_room(self):
        new_room = MessageRoom.objects.create(name='test_room', owner=self.user_one)
        new_room.save()
        url = f'http://localhost:8000/message/add/user/{self.user_two.id}/room/{new_room.id}'
        response = self.client_user_one.post(url)
        user_in_room_id = response.data['id']
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(UserInRoom.objects.filter(id=user_in_room_id).exists(), True)
        print(f"{OKGREEN}user addition to a room test passed !{ENDC}")

    def test_wrong_user_room_addition(self):
        new_room = MessageRoom.objects.create(name='test_room', owner=self.user_one)
        new_room.save()
        # there is no user with id 230
        url = f'http://localhost:8000/message/add/user/230/room/{new_room.id}'
        response = self.client_user_one.post(url)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        print(f"{OKGREEN}wrong user addition to a room test passed !{ENDC}")

    def test_wrong_room_addition(self):
        new_room = MessageRoom.objects.create(name='test_room', owner=self.user_one)
        new_room.save()
        # there is no room with id 200
        url = f'http://localhost:8000/message/add/user/{self.user_two.id}/room/200'
        response = self.client_user_one.post(url)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        print(f"{OKGREEN}user addition to a wrong room test passed !{ENDC}")

    def test_not_member_of_room_adds_user_to_room(self):
        new_room = MessageRoom.objects.create(name='test_room', owner=self.user_one)
        new_room.save()
        url = f'http://localhost:8000/message/add/user/{self.user_two.id}/room/{new_room.id}'
        response = self.client_user_two.post(url)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        print(response.data)
        print(f"{OKGREEN}not member trying to add a user to a room test passed !{ENDC}")

    def test_user_duplicate_addition(self):
        new_room = MessageRoom.objects.create(name='test_room', owner=self.user_one)
        new_room.save()
        UIR = UserInRoom.objects.create(room=new_room, user=self.user_two)
        # add user_two to new_room again !
        url = f'http://localhost:8000/message/add/user/{self.user_two.id}/room/{new_room.id}'
        response = self.client_user_one.post(url)
        print(response.data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        print(f"{OKGREEN}duplicate user addition test passed!{ENDC}")

    def test_message_creation(self):
        new_room = MessageRoom.objects.create(name='test_room', owner=self.user_one)
        new_room.save()
        data = {
            'sender': self.user_one.id,
            'message': 'test Message !',
            'reciever_room' : new_room.id
        }
        response = self.client_user_one.post(self.message_viewSet_url, data)
        print(response.data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        message_id = response.data['id']
        self.assertEquals(Message.objects.filter(id=message_id).exists(), True)

        retrieve_message = self.client_user_one.get(f"{self.message_viewSet_url}{message_id}/")
        self.assertEquals(retrieve_message.status_code, status.HTTP_200_OK)
        self.assertEquals(retrieve_message.data['message'], 'test Message !')

        list_of_messages = self.client_user_one.get(f"{self.message_viewSet_url}")
        self.assertEquals(len(list_of_messages.data), 1)
        print(f"{OKGREEN}message creation test passed!{ENDC}")

    def test_chat_all_messages(self):
        # new room
        new_room = MessageRoom.objects.create(name='test_room', owner=self.user_one)
        new_room.save()
        # add user in the room
        UIR = UserInRoom.objects.create(user=self.user_one, room=new_room)
        UIR.save()
        # send a message in it
        new_message = Message.objects.create(sender=self.user_one, reciever_room=new_room, message='Test Message')
        # get all messages of the new room
        url = f'http://localhost:8000/message/room/chats/{new_room.id}'
        response = self.client_user_one.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 1)
        self.assertEquals(response.data[0].get('message'), 'Test Message')
        print(f"{OKGREEN}get all messages of a chat test passed!{ENDC}")

    def test_bad_permission_of_chat_all_messages(self):
        '''
            scenario : a user out of a room wants to see all messages of the room.
            The user do not have permission to perform this action.
        '''

        # new room
        new_room = MessageRoom.objects.create(name='test_room', owner=self.user_one)
        new_room.save()
        # add user in the room
        UIR = UserInRoom.objects.create(user=self.user_one, room=new_room)
        UIR.save()
        # send a message in it
        new_message = Message.objects.create(sender=self.user_one, reciever_room=new_room, message='Test Message')
        # get all messages of the new room
        url = f'http://localhost:8000/message/room/chats/{new_room.id}'
        response = self.client_user_two.get(url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        print(f"{OKGREEN}get all messages of chat permission test passed!{ENDC}")