from django.test import TestCase
from rest_framework.test import APIClient
import json
from django.urls import reverse
from rest_framework import status
from ..models import *

class UserInformationTest(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username="morteza", email="morteza@gmail.com")
        self.user.set_password("mo1234")
        self.user.save()
        
    def login(self, username, password):
        # print(username, password)
        url = reverse('accounts:accounts-jwt-create')
        data = json.dumps({'username': username, 'password': password})
        response = self.client.post(url, data, content_type='application/json')
        if response.status_code == status.HTTP_200_OK:
            access_token = response.data['access']
            return access_token
        else:
            return "incorrect"
        

    def test_correct_user_informations(self):
        
        access_token = self.login("morteza", "mo1234")
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + access_token)
        url = reverse('accounts:user-information')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    def test_incorrect_user_informations_without_token(self):
        
        url = reverse('accounts:user-information')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        
    def test_incorrect_user_informations_incorrect_token(self):
        
        access_token = self.login("morteza", "mo1234")
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + access_token + 'abcd')
        url = reverse('accounts:user-information')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)