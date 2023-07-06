from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django import urls
import json
from django.http import HttpRequest
from rest_framework import permissions, status
from rest_framework.response import Response
from ..models import *
from django.urls import reverse
import mock


class AdminViewSetTestCase(TestCase):
    
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
        user = User.objects.create(username=username, email=email)
        user.set_password(password)
        user.save()
        return user
    
    
    def setUp(self):
        self.admin = User.objects.create(
            email="admin@gmail.com",
            username="admin",
            first_name="سید عماد",
            last_name="موسوی",
            phone_no="09364945328",
            is_admin=True
        )
        self.admin.set_password('admin')
        self.admin.is_admin = True
        self.admin.save()
        self.client = APIClient()
        
        self.user = self.make_user('amir', '123456', 'amir@gmail.com')
        self.sp_user = SpecialUser.objects.create(user=self.user)
        
        self.normal_user = self.make_user('normal', '123456', 'normal@gmail.com')


    @classmethod
    def setUpTestData(cls):
        return super().setUpTestData()

    def test_addAdmin(self):
        token = self.login(self.admin.username, 'admin')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        url = 'http://127.0.0.1:8000/accounts/admin/add-admin/'
        response = self.client.post(path=url, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_incorrect_addAdmin_without_token(self):
        url = 'http://127.0.0.1:8000/accounts/admin/add-admin/'
        response = self.client.post(path=url, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    
    def test_removeSpecialUser(self):
        token = self.login(self.admin.username, 'admin')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        url = 'http://127.0.0.1:8000/accounts/admin/remove-specialuser/'
        data = {
            "username": self.user.username
        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
    def test_removeSpecialUser_user_not_exist(self):
        token = self.login(self.admin.username, 'admin')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        url = 'http://127.0.0.1:8000/accounts/admin/remove-specialuser/'
        data = {
            "username": "normal"
        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_removeUser(self):
        url = 'http://127.0.0.1:8000/accounts/admin/remove-user/'
        token = self.login(self.admin.username, 'admin')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            "username": self.normal_user.username
        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_removeUser_no_username(self):
        url = 'http://127.0.0.1:8000/accounts/admin/remove-user/'
        token = self.login(self.admin.username, 'admin')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {}
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_removeUser_admin_user(self):
        url = 'http://127.0.0.1:8000/accounts/admin/remove-user/'
        token = self.login(self.admin.username, 'admin')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            "username": self.admin.username
        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS)
        

    def test_addUser(self):
        url = 'http://127.0.0.1:8000/accounts/admin/add-user/'
        token = self.login(self.admin.username, 'admin')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            "username": "newUser",
            "email": "new@gmail.com",
            "password": "123456",
            "re_password": "123456"
        }
        response = self.client.post(url, data=data, format='json')   
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
    def test_addUser_no_username(self):
        url = 'http://127.0.0.1:8000/accounts/admin/add-user/'
        token = self.login(self.admin.username, 'admin')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            "email": "new@gmail.com",
            "password": "123456",
            "re_password": "123456"
        }
        response = self.client.post(url, data=data, format='json')   
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_addUser_no_email(self):
        url = 'http://127.0.0.1:8000/accounts/admin/add-user/'
        token = self.login(self.admin.username, 'admin')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            "username": "newUser",
            "password": "123456",
            "re_password": "123456"
        }
        response = self.client.post(url, data=data, format='json')   
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    
    def test_addUser_no_password(self):
        url = 'http://127.0.0.1:8000/accounts/admin/add-user/'
        token = self.login(self.admin.username, 'admin')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            "username": "newUser",
            "email": "new@gmail.com",
            "re_password": "123456"
        }
        response = self.client.post(url, data=data, format='json')   
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    
    def test_addUser_not_matching_password(self):
        url = 'http://127.0.0.1:8000/accounts/admin/add-user/'
        token = self.login(self.admin.username, 'admin')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            "username": "newUser",
            "email": "new@gmail.com",
            "password": "123456",
            "re_password": "1234567"
        }
        response = self.client.post(url, data=data, format='json')   
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
