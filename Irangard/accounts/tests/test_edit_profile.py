from django.test import TestCase
from django.urls import reverse
from accounts.models import User
from rest_framework.test import APIClient
import json
from rest_framework import status


# Create your tests here.
class TestUserProfile(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username="morteza")
        self.user.set_password("mo1234")
        self.user.save()
        
    def test_getProfile(self):
        response = self.client.get(reverse('accounts:user-profile', args=(self.user.username,)))
        self.assertEqual(response.status_code, 200)
        
    def test_login(self):
        url = reverse('accounts:accounts-jwt-create')
        response = self.client.post(url, {"username":"morteza","password":"mo1234"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
