from django.test import TestCase, Client
from ..models import TourSuggestion, EventSuggestion, PlaceSuggestion
from accounts.models import User, SpecialUser
from tours.models import Tour
from rest_framework.test import APIClient
from django.urls import reverse
import json
from rest_framework import status
import io
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
import base64
import json
from django.utils.dateparse import parse_date
import datetime


class TourSuggestionViewsTestCase(TestCase):
    
    def make_user(self, username, password, email):
        user = User.objects.create_user(username, email, password)
        return user
    
    
    def make_super_user(self, username, password, email):
        user = User.objects.create_user(username, email, password)
        user.is_superuser = True
        user.save()
        return user
    
    
    def make_tour(self):
        data = {
            "title": "test_tour",
            "cost": 200,
            "capacity": 50,
            "remaining": 50,
            "start_date": "2022-05-22T15:49:49.505Z",
            "end_date": "2022-05-23T15:49:49.505Z"
        }
        tour = Tour.objects.create(**data, owner = self.special_user)
        return tour


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
        self.url = 'http://127.0.0.1:8000/suggestion/tour/'
        self.user = self.make_user('amir', '123456', 'amir@gmail.com')
        self.special_user = SpecialUser.objects.create(
            user=self.user, total_revenue=0)
        self.user1 = self.make_user('ali', '123456','ali@gmail.com')
        self.user2 = self.make_user('amin', '123456', 'amin@gmail.com')
        self.user3 = self.make_user('armin', '123456', 'armin@gmail.com')
        self.tour = self.make_tour()
        self.cheater_user = self.make_user("cheater", "123456", "cheater@gmail.com")
        self.super_user = self.make_super_user("superuser", "123456", "super@gmail.com")
        self.tour_suggestion = TourSuggestion.objects.create(
            sender=self.user1, 
            receiver=self.user2, 
            tour=self.tour, 
            text="test"
        )
        
    
    def test_correct_get_tour_suggestions_super_user(self):
        token = self.login(self.super_user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
          
    
    def test_incorrect_get_tour_suggestions_normal_user(self):
        token = self.login(self.user1.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    
    def test_correct_retrieve_tour_suggestion_sender_user(self):
        token = self.login(self.user1.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(self.url + str(self.tour_suggestion.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
    def test_correct_retrieve_tour_suggestion_receiver_user(self):
        token = self.login(self.user2.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(self.url + str(self.tour_suggestion.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    
    def test_correct_retrieve_tour_suggestion_super_user(self):
        token = self.login(self.super_user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(self.url + str(self.tour_suggestion.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
    def test_incorrect_retrieve_tour_suggestion_cheater_user(self):
        token = self.login(self.cheater_user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(self.url + str(self.tour_suggestion.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    
    def test_correct_post_tour_suggestion(self):
        for i in TourSuggestion.objects.all():
            print(str(i))
        # print(TourSuggestion.objects.all())
        token = self.login(self.user2.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            "receiver": self.user3.pk,
            "text": "test",
            "tour": self.tour.pk
        }
        response = self.client.post(self.url, data=data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    
    def test_correct_post_tour_suggestion_ignore_sender_field(self):
        token = self.login(self.user2.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            "sender": 10000,
            "receiver": self.user3.pk,
            "text": "test",
            "tour": self.tour.pk
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    
    def test_incorrect_post_without_token(self):
        data = {
            "receiver": self.user3.pk,
            "text": "test",
            "tour": self.tour.pk
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    
    def test_incorrect_post_repetitive_sender_receiver_tour(self):
        token = self.login(self.user1.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            "receiver": self.user2.pk,
            "text": "test",
            "tour": self.tour.pk
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    
    def test_incorrect_post_same_sender_receiver(self):
        token = self.login(self.user1.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            "receiver": self.user1.pk,
            "text": "test",
            "tour": self.tour.pk
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    
    