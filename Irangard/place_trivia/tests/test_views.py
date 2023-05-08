from django.test import TestCase, Client
from places.models import Contact, Place
from tours.models import Tour
from events.models import Event
from accounts.models import SpecialUser, User
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status


class PlaceTriviaViewTestcase(TestCase):
    
    def make_tour(self, province, city):
        data = {
            "title": "test_tour",
            "cost": 200,
            "capacity": 50,
            "remaining": 50,
            "start_date": "2022-05-22T15:49:49.505Z",
            "end_date": "2022-05-23T15:49:49.505Z"
        }
        tour = Tour.objects.create(**data, owner=self.special_user)
        return tour
    
    
    def make_place(self, province, city):
        place = Place.objects.create(
            place_type=1, title="test place", 
            description="test description", added_by=self.user)
        Contact.objects.create(
            place=place, 
            x_location=0, 
            y_location=0, 
            province=province, 
            city=city
        )
        return place
    
    
    def make_event(self, province, city):
        event = Event.objects.create(
            event_type='0', event_category='0', title='test event', 
            organizer='test organizer', description='test description', 
            x_location=0, y_location=0, start_date='2022-05-22', 
            end_date='2022-05-23', start_time='00:00:00', end_time='00:00:00',
            added_by=self.user, address='test address', is_free=True,
            province=province, city=city, website='www.org.com', 
            phone='09109530195')
        return event
    
    
    def make_user(self, username, password, email):
        user = User.objects.create_user(username, email, password)
        return user
    
    
    def setUp(self):
        self.client = APIClient()
        self.url = 'http://127.0.0.1:8000/place_trivia/'
        
        self.user = self.make_user('amir', 'amir@gmail.com', '123456')
        self.special_user = SpecialUser.objects.create(
            user=self.user, total_revenue=0)
        
        self.tour1 = self.make_tour('Tehran', 'Tehran')
        self.tour2 = self.make_tour('Tehran', 'Tehran')
        self.tour3 = self.make_tour('Mazandaran', 'Qaemshahr')
        
        self.place1 = self.make_place('Tehran', 'Tehran')
        self.place2 = self.make_place('Tehran', 'Tehran')
        self.place3 = self.make_place('Mazandaran', 'Qaemshahr')
        
        self.event1 = self.make_event('Tehran', 'Tehran')
        self.event2 = self.make_event('Tehran', 'Tehran')
        self.event3 = self.make_event('Mazandaran', 'Qaemshahr')    
    
    
    def get_place_trivia(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = response.json()
        self.assertIn('tours', response_json.keys())
        self.assertIn('events', response_json.keys())
        self.assertIn('places', response_json.keys())

    
    def get_place_trivia_province_filter(self):
        response = self.client.get(self.url + 'province/Tehran/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(response.data, 'tours')
        self.assertIn(response.data, 'events')
        self.assertIn(response.data, 'places')
        
        for tour in response.data['tours']:
            self.assertEqual(tour.province, 'Tehran')
        
        for place in response.data['places']:
            self.assertEqual(place.contact.province, 'Tehran')
        
        for event in response.data['events']:
            self.assertEqual(event.province, 'Tehran')
    
    
    def get_place_trivia_city_filter(self):
        response = self.client.get(self.url + 'city/Tehran/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(response.data, 'tours')
        self.assertIn(response.data, 'events')
        self.assertIn(response.data, 'places')

        for tour in response.data['tours']:
            self.assertEqual(tour.city, 'Tehran')
        
        for place in response.data['places']:
            self.assertEqual(place.contact.city, 'Tehran')
        
        for event in response.data['events']:
            self.assertEqual(event.city, 'Tehran')
    