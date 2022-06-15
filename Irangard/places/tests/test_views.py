from django.test import TestCase, Client
from rest_framework import status
from django.urls import reverse
from ..models import *
from accounts.models import User
from email.mime import image
from rest_framework.test import APIClient
import io
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
import json

client = Client()

class PlaceViewsTestCase(TestCase):
       
    def make_user(self, username, password, email):
        self.user = User.objects.create(username=username, email=email)
        self.user.set_password(password)
        self.user.save()
        return self.user
    
    def login(self, username, password):
        url = reverse('accounts:accounts-jwt-create')
        data = json.dumps({'username': username, 'password': password})
        response = self.client.post(url, data, content_type='application/json')
        if response.status_code == status.HTTP_200_OK:
            access_token = response.data['access']
            return access_token
        else:
            return "incorrect"
    
    def setUp(self):
        self.client = APIClient()
        self.url = 'http://127.0.0.1:8000/places/'
        self.user = self.make_user("ghazal", "gh1234", "ghazal@gmail.com")
        self.place = Place.objects.create(
            place_type=1, title="test place", description="test_description", added_by=self.user)
    
    def post_place(self, data, user):     
        token = self.login(self.user.username, 'gh1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)      
        response = self.client.post(self.url, data=data)
        return response.data
    
    def test_get_places(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_correct_retrieve_place(self):
        retrieve_url = self.url + str(self.place.id) + '/'
        response = self.client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_incorrect_retrieve_place(self):
        retrieve_url = self.url + str(2000) + '/'
        response = self.client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_404_BAD_REQUEST)
        
    def test_correct_post_place(self):
        
        token = self.login(self.user.username, 'gh1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        
        data = {
            "title": "new place",
            "description": "new place description",
            "place_type": 0,
            "is_free": True,
        }

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_incorrect_post_place_without_token(self):
        
        data = {
            "title": "new place",
            "description": "new place description",
            "place_type": 0,
            "is_free": True,
        }

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        
    def test_incorrect_post_place_incorrect_token(self):
        
        token = self.login(self.user.username, 'gh1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token + 'aa')
        
        data = {
            "title": "new place",
            "description": "new place description",
            "place_type": 0,
            "is_free": True,
        }

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_incorrect_post_place_without_title(self):
        
        token = self.login(self.user.username, 'gh1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        
        data = {
            "description": "new place description",
            "place_type": 0,
            "is_free": True,
        }

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        

    def test_correct_post_place_without_description(self):
        
        token = self.login(self.user.username, 'gh1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
   
        data = {
            "title": "new place",
            "place_type": 0,
            "is_free": True,
        }

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_correct_post_place_without_is_free(self):
        
        token = self.login(self.user.username, 'gh1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
   
        data = {
            "title": "new place",
            "description": "new place description",
            "place_type": 0,
        }

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
   
        
    def test_incorrect_post_place_without_place_type(self):
        
        token = self.login(self.user.username, 'gh1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        
        data = {
            "title": "new place",
            "description": "new place description",
            "is_free": True,
        }

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        
    def test_correct_put_place(self):
        
        token = self.login(self.user.username, 'gh1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        
        data = {
            "title": "new updated place",
            "description": "new updated place description",
            "place_type": 1,
            "is_free": False,
        }

        put_url = self.url + str(self.place.id) + '/'
        response = self.client.put(put_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    def test_incorrect_put_place_without_token(self):
        
        data = {
            "title": "new updated place",
            "description": "new updated place description",
            "place_type": 1,
            "is_free": False,
        }

        put_url = self.url + str(self.place.id) + '/'
        response = self.client.put(put_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        
    def test_incorrect_put_place_incorrect_token(self):
        
        token = self.login(self.user.username, 'gh1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token + 'aa')
        
        data = {
            "title": "new updated place",
            "description": "new updated place description",
            "place_type": 1,
            "is_free": False,
        }
        
        put_url = self.url + str(self.place.id) + '/'
        response = self.client.put(put_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        
    def test_incorrect_put_place_invalid_token(self):
        
        new_user = self.make_user("ghazal-new", "gh1234-new", "ghazal-new@gmail.com")
        
        token = self.login("ghazal-new", "gh1234-new")
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        
        data = {
            "title": "new updated place",
            "description": "new updated place description",
            "place_type": 1,
            "is_free": False,
        }

        put_url = self.url + str(self.place.id) + '/'
        response = self.client.put(put_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
         
        
    def test_incorrect_put_place_without_title(self):
        
        token = self.login(self.user.username, 'gh1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
 
        data = {
            "description": "new updated place description",
            "place_type": 1,
            "is_free": False,
        }

        put_url = self.url + str(self.place.id) + '/'
        response = self.client.put(put_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        
    def test_correct_put_place_without_description(self):
        
        token = self.login(self.user.username, 'gh1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        
        data = {
            "title": "new updated place",
            "place_type": 1,
            "is_free": False,
        }

        put_url = self.url + str(self.place.id) + '/'
        response = self.client.put(put_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_correct_put_place_without_is_free(self):
        
        token = self.login(self.user.username, 'gh1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        
        data = {
            "title": "new updated place",
            "description": "new updated place description",
            "place_type": 1,
        }

        put_url = self.url + str(self.place.id) + '/'
        response = self.client.put(put_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

    def test_incorrect_put_place_without_place_type(self):
        
        token = self.login(self.user.username, 'gh1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
 
        data = {
            "title": "new updated place",
            "description": "new updated place description",
            "is_free": False,
        }

        put_url = self.url + str(self.place.id) + '/'
        response = self.client.put(put_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        
    def test_correct_delete_place(self):
        
        token = self.login(self.user.username, 'gh1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        delete_url = self.url + str(self.place.id) + '/'
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    
    def test_incorrect_delete_place_without_token(self):
        
        delete_url = self.url + str(self.place.id) + '/'
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        
    def test_incorrect_delete_place_incorret_token(self):
        
        token = self.login(self.user.username, 'gh1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token + 'abc')
        delete_url = self.url + str(self.place.id) + '/'
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        
    def test_incorrect_delete_place_invalid_token(self):
        
        new_user = self.make_user("ghazal-new", "gh1234-new", "ghazal-new@gmail.com")
        
        token = self.login("ghazal-new", "gh1234-new")
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        delete_url = self.url + str(self.place.id) + '/'
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

