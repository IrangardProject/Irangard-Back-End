from django.test import TestCase, Client
from accounts.models import User
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
import base64
import json


class PlaceTriviaViewTestcase(TestCase):
    
    def make_tour(self):
        pass
    
    
    def make_place(self):
        pass
    
    
    def make_event(self):
        pass
    
    
    def make_user(self):
        pass
    
    
    def setUp(self):
        self.client = APIClient()
        self.url = 'http://127.0.0.1:8000/place_trivia/'
        
        self.user = self.make_user()

        self.tour1 = self.make_tour()
        self.tour2 = self.make_tour()
        self.tour3 = self.make_tour()
        
        self.place1 = self.make_place()
        self.place2 = self.make_place()
        self.place3 = self.make_place()
        
        self.event1 = self.make_event()
        self.event2 = self.make_event()
        self.event3 = self.make_event()
        
    
    def get_place_trivia(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(response.data, 'tours')
        self.assertIn(response.data, 'events')
        self.assertIn(response.data, 'places')
    
    
    def get_place_trivia_province_filter(self):
        response = self.client.get(self.url + 'province/tehran/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(response.data, 'tours')
        self.assertIn(response.data, 'events')
        self.assertIn(response.data, 'places')
    
    
    def get_place_trivia_city_filter(self):
        response = self.client.get(self.url + 'city/tehran/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictContainsSubset(response.data, 'tours')
        self.assertDictContainsSubset(response.data, 'events')
        self.assertDictContainsSubset(response.data, 'places')
    