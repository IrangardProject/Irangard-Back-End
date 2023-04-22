from django.test import TestCase
from ..models import Event, Tag, Image
from accounts.models import User
from rest_framework.test import APIClient
from django.urls import reverse
import json
from rest_framework import status
from django.utils.dateparse import parse_date
import datetime


class EventTestcase(TestCase):
    
    
    def make_user(self):
        self.user = User.objects.create(username="amir", email="amir@gmail.com")
        self.user.set_password("123456")
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
        self.user = self.make_user()
        token = self.login(self.user.username, self.user.password)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        Event.objects.create(
            event_type='0', event_category='0', title='test event', 
            organizer='test organizer', description='test description', 
            x_location=0, y_location=0, start_date='2022-05-22', 
            end_date='2022-05-23', start_time='00:00:00', end_time='00:00:00',
            added_by=self.user, address='test address', is_free=True,
            province='تهران', city='تهران', website='www.org.com', 
            phone='09109530195')
        
    
    def test_title(self):
        event = Event.objects.get(title="test event")
        self.assertEqual(event.title, "test event")
        
    
    def test_event_type(self):
        event = Event.objects.get(title="test event")
        self.assertEqual(event.event_type, "0")
        
    
    def test_event_category(self):
        event = Event.objects.get(title="test event")
        self.assertEqual(event.event_category, "0")
        
    
    def test_organizer(self):
        event = Event.objects.get(title="test event")
        self.assertEqual(event.organizer, "test organizer")
    
    
    def test_description(self):
        event = Event.objects.get(title="test event")
        self.assertEqual(event.description, "test description")
        
    
    def test_x_location(self):
        event = Event.objects.get(title="test event")
        self.assertEqual(event.x_location, 0)
    
    
    def test_y_location(self):
        event = Event.objects.get(title="test event")
        self.assertEqual(event.y_location, 0)
    
    
    def test_address(self):
        event = Event.objects.get(title="test event")
        self.assertEqual(event.address, 'test address')
    
    
    def test_start_date(self):
        event = Event.objects.get(title="test event")
        self.assertEqual(event.start_date, parse_date('2022-05-22'))
        
        
    def test_end_date(self):
        event = Event.objects.get(title="test event")
        self.assertEqual(event.end_date, parse_date('2022-05-23'))
        
        
    def test_start_time(self):
        event = Event.objects.get(title="test event")
        self.assertEqual(event.start_time, datetime.time(0, 0))
        
        
    def test_end_time(self):
        event = Event.objects.get(title="test event")
        self.assertEqual(event.end_time, datetime.time(0, 0))
        
    
    def test_added_by(self):
        event = Event.objects.get(title="test event")
        self.assertEqual(event.added_by, self.user)
        
    
    def test_province(self):
        event = Event.objects.get(title="test event")
        self.assertEqual(event.province, "تهران")
        
        
    def test_city(self):
        event = Event.objects.get(title="test event")
        self.assertEqual(event.city, "تهران")
        
    
    def test_website(self):
        event = Event.objects.get(title="test event")
        self.assertEqual(event.website, "www.org.com")
    
    
    def test_city(self):
        event = Event.objects.get(title="test event")
        self.assertEqual(event.phone, "09109530195")
        

class TagTestCase(TestCase):
    
    def make_user(self):
        self.user = User.objects.create(username="amir", email="amir@gmail.com")
        self.user.set_password("123456")
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
        self.user = self.make_user()
        token = self.login(self.user.username, self.user.password)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        self.event = Event.objects.create(
            event_type='0', event_category='0', title='test event', 
            organizer='test organizer', description='test description', 
            x_location=0, y_location=0, start_date='2022-05-22', 
            end_date='2022-05-23', start_time='00:00:00', end_time='00:00:00',
            added_by=self.user, address='test address', is_free=True,
            province='تهران', city='تهران',  website='www.org.com',
            phone='09109530195')
        Tag.objects.create(event=self.event, name="test tag")

        
    def test_name(self):
        tag = Tag.objects.get(event=self.event)
        self.assertEqual(tag.name, "test tag")
        