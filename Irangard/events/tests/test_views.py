from django.test import TestCase
from ..models import Event
from accounts.models import User
from rest_framework.test import APIClient
from django.urls import reverse
import json
from rest_framework import status
import io
from PIL import Image
import base64
import json
from django.utils.dateparse import parse_date
import datetime
from utils.constants import StatusMode, ActionDimondExchange


class EventViewsTestcase(TestCase):
    
    def make_user(self, username, password, email):
        user = User.objects.create(username=username, email=email)
        user.set_password(password)
        user.save()
        return user
    
    
    def make_admin_user(self, username, password, email):
        user = User.objects.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
    
    
    def login(self, username, password):
        url = reverse('accounts:accounts-jwt-create')
        data = json.dumps({'username': username, 'password': password})
        response = self.client.post(url, data, content_type='application/json')
        if response.status_code == status.HTTP_200_OK:
            access_token = response.data['access']
            return access_token
        else:
            return "incorrect"
    
    
    def temporary_image(self):
        bts = io.BytesIO()
        img = Image.new("RGB", (100, 100))
        img.save(bts, 'jpeg')
        image_data = bts.getvalue()
        encoded_data = base64.b64encode(image_data).decode('utf-8')
        return encoded_data
    
    
    def setUp(self):
        self.client = APIClient()
        self.url = 'http://127.0.0.1:8000/events/'
        self.user = self.make_user("amir", "123456", "amir@gmail.com")
        self.cheater_user = self.make_user("cheater", "123456", "cheater@gmail.com")
        self.admin_user = self.make_admin_user("admin", "123456", "admin@gmail.com")
        
        self.event = Event.objects.create(
            event_type='0', event_category='0', title='test event', 
            organizer='test organizer', description='test description', 
            x_location=0, y_location=0, start_date='2030-05-22', 
            end_date='2030-05-23', start_time='00:00:00', end_time='00:00:00',
            added_by=self.user, address='test address', is_free=True,
            province='تهران', city='تهران',  website='www.org.com', 
            phone='09109530195', status=StatusMode.ACCEPTED
        )
        
        self.event_not_active = Event.objects.create(
            event_type='0', event_category='0', title='test event', 
            organizer='test organizer', description='test description', 
            x_location=0, y_location=0, start_date='2030-05-22', 
            end_date='2030-05-23', start_time='00:00:00', end_time='00:00:00',
            added_by=self.user, address='test address', is_free=True,
            province='تهران', city='تهران',  website='www.org.com', 
            phone='09109530195'
        )
        
        
        self.tags = [
            {
                "name": "test 1"
            },
            {
                "name": "test 2"
            },
            {
                "name": "test 3"
            }
        ]
        
        self.data = {
            "event_type": "0",
            "event_category": "0",
            "title": "test post event", 
            "organizer": "test organizer", 
            "description": "test description", 
            "x_location": 0, 
            "y_location": 0, 
            "start_date": "2030-05-22", 
            "end_date": "2030-05-23",
            "start_time": "00:00:00",
            "end_time": "00:00:00", 
            "added_by": self.user.pk,
            "province": "تهران",
            "city": "تهران",
            "tags": self.tags,
            "address": "test address",
            "is_free": 1,
            "website": "www.org.com",
            "phone": "09109530195"
        }

        self.updating_tags = [
            {
                "name": "test 1"
            },
            {
                "name": "test 2"
            }
        ]
        
        self.updating_data = {
            "event_type": "1",
            "event_category": "1",
            "title": "test post event updated", 
            "organizer": "test organizer updated", 
            "description": "test description updated", 
            "x_location": 1, 
            "y_location": 1, 
            "start_date": "2030-05-23", 
            "end_date": "2030-05-24",
            "start_time": "01:00:00",
            "end_time": "01:00:00", 
            "added_by": self.cheater_user.pk,
            "province": "قم",
            "city": "قم",
            "tags": self.updating_tags,
            "address": "test address updated",
            "is_free": 0,
            "website": "www.org.com",
            "phone": "09109530195"
        }
    
    
    def test_correct_post_event(self):     
        token = self.login(self.user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.post(self.url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    
    def test_correct_post_event_ignore_status_field(self):
        token = self.login(self.user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = self.data.copy()
        data["status"] = StatusMode.ACCEPTED
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        event = Event.objects.get(title="test post event")
        self.assertEqual(event.status, StatusMode.PENDING)
    
    
    def test_incorrect_post_events_without_token(self):
        response = self.client.post(self.url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    
    def test_correct_get_events_with_token(self):
        token = self.login(self.user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
    def test_correct_get_events_without_token(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    
    def test_correct_retrieve_event_with_token(self):
        token = self.login(self.user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get("{}{}/".format(self.url, self.event.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    
    def test_correct_retrieve_event_without_token(self):
        response = self.client.get("{}{}/".format(self.url, self.event.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
    def test_correct_update_event(self):
        token = self.login(self.user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.put("{}{}/".format(self.url, self.event.pk),
                                data=self.updating_data, format='json')
        self.event.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.event.event_type, "1")
        self.assertEqual(self.event.event_category, "1")
        self.assertEqual(self.event.title, "test post event updated")
        self.assertEqual(self.event.organizer, "test organizer updated")
        self.assertEqual(self.event.description, "test description updated")
        self.assertEqual(self.event.x_location, 1)
        self.assertEqual(self.event.y_location, 1)
        self.assertEqual(self.event.start_date, parse_date("2030-05-23"))
        self.assertEqual(self.event.end_date, parse_date("2030-05-24"))
        self.assertEqual(self.event.start_time, datetime.time(1, 0))
        self.assertEqual(self.event.end_time, datetime.time(1, 0))
        self.assertEqual(self.event.province, "قم")
        self.assertEqual(self.event.city, "قم")
        self.assertEqual(len(self.event.tags.all()), 2)
        self.assertEqual(self.event.address, "test address updated")
        self.assertEqual(self.event.is_free, False)
    
    
    def test_correct_update_event_ignore_status_field(self):
        token = self.login(self.user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = self.updating_data.copy()
        data["staus"] = StatusMode.DENIED
        response = self.client.put("{}{}/".format(self.url, self.event.pk),
                                data=self.updating_data, format='json')
        self.event.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.event.event_type, "1")
        self.assertEqual(self.event.event_category, "1")
        self.assertEqual(self.event.title, "test post event updated")
        self.assertEqual(self.event.organizer, "test organizer updated")
        self.assertEqual(self.event.description, "test description updated")
        self.assertEqual(self.event.x_location, 1)
        self.assertEqual(self.event.y_location, 1)
        self.assertEqual(self.event.start_date, parse_date("2030-05-23"))
        self.assertEqual(self.event.end_date, parse_date("2030-05-24"))
        self.assertEqual(self.event.start_time, datetime.time(1, 0))
        self.assertEqual(self.event.end_time, datetime.time(1, 0))
        self.assertEqual(self.event.province, "قم")
        self.assertEqual(self.event.city, "قم")
        self.assertEqual(len(self.event.tags.all()), 2)
        self.assertEqual(self.event.address, "test address updated")
        self.assertEqual(self.event.is_free, False)
        self.assertEqual(self.event.status, StatusMode.ACCEPTED)
        
    
    def test_correct_update_pending_event(self):
        token = self.login(self.user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.put("{}{}/".format(self.url, self.event_not_active.pk),
                                data=self.updating_data, format='json')
        self.event_not_active.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.event_not_active.event_type, "1")
        self.assertEqual(self.event_not_active.event_category, "1")
        self.assertEqual(self.event_not_active.title, "test post event updated")
        self.assertEqual(self.event_not_active.organizer, "test organizer updated")
        self.assertEqual(self.event_not_active.description, "test description updated")
        self.assertEqual(self.event_not_active.x_location, 1)
        self.assertEqual(self.event_not_active.y_location, 1)
        self.assertEqual(self.event_not_active.start_date, parse_date("2030-05-23"))
        self.assertEqual(self.event_not_active.end_date, parse_date("2030-05-24"))
        self.assertEqual(self.event_not_active.start_time, datetime.time(1, 0))
        self.assertEqual(self.event_not_active.end_time, datetime.time(1, 0))
        self.assertEqual(self.event_not_active.province, "قم")
        self.assertEqual(self.event_not_active.city, "قم")
        self.assertEqual(len(self.event_not_active.tags.all()), 2)
        self.assertEqual(self.event_not_active.address, "test address updated")
        self.assertEqual(self.event_not_active.is_free, False)
    
    
    def test_incorrect_update_event_without_token(self):   
        response = self.client.put("{}{}/".format(self.url, self.event.pk),
                                data=self.updating_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    
    def test_incorrect_update_event_wrong_user_token(self):
        token = self.login(self.cheater_user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.put("{}{}/".format(self.url, self.event.pk),
                                data=self.updating_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    
    def test_correct_patch_event(self):
        token = self.login(self.user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        
        data = {
            "event_type": "1"
        }
        
        response = self.client.patch("{}{}/".format(self.url, self.event.pk), data=data)
        self.event.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.event.event_type, "1")

        
    def test_incorrect_patch_event_without_token(self):
        data = {
            "event_type": "1"
        }
        
        response = self.client.patch("{}{}/".format(self.url, self.event.pk), data=data)
        self.event.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        
    def test_incorrect_patch_event_wrong_user_token(self):
        token = self.login(self.cheater_user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        
        data = {
            "event_type": "1"
        }
        
        response = self.client.patch("{}{}/".format(self.url, self.event.pk), data=data)
        self.event.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        
    def test_correct_delete_event(self):
        token = self.login(self.user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        
        response = self.client.delete("{}{}/".format(self.url, self.event.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        
    def test_incorrect_delete_without_token(self):
        response = self.client.delete("{}{}/".format(self.url, self.event.pk))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        
    def test_incorrect_patch_event_wrong_user_token(self):
        token = self.login(self.cheater_user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.delete("{}{}/".format(self.url, self.event.pk))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    
    def test_correct_accept_event_admin_user(self):
        user_dimond_before_activate = self.event_not_active.added_by.dimonds
        token = self.login(self.admin_user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.put(f"{self.url}{self.event_not_active.pk}/admin_acceptance/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.event_not_active.refresh_from_db()
        self.assertEqual(self.event_not_active.status, StatusMode.ACCEPTED)
        self.assertEqual(user_dimond_before_activate + ActionDimondExchange.ADDING_EVENT, 
                        self.event_not_active.added_by.dimonds
                    )
        
    
    
    def test_incorrect_accept_event_without_token(self):
        response = self.client.put(f"{self.url}{self.event_not_active.pk}/admin_acceptance/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    
    def test_incorrect_accept_event_normal_user_token(self):
        token = self.login(self.user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.put(f"{self.url}{self.event_not_active.pk}/admin_acceptance/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    
    def test_correct_deny_event_admin_user(self):
        token = self.login(self.admin_user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.put(f"{self.url}{self.event_not_active.pk}/admin_denial/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.event_not_active.refresh_from_db()
        self.assertTrue(self.event_not_active.status, StatusMode.ACCEPTED)
    
    
    def test_incorrect_deny_event_without_token(self):
        response = self.client.put(f"{self.url}{self.event_not_active.pk}/admin_denial/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    
    def test_incorrect_deny_event_normal_user_token(self):
        token = self.login(self.user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.put(f"{self.url}{self.event_not_active.pk}/admin_denial/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    
    def test_correct_get_pending_events_admin_user(self):
        token = self.login(self.admin_user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(f"{self.url}pending_events/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for event in response.data:
            self.assertEqual(event["status"], StatusMode.PENDING)

    
    def test_incorrect_get_pending_events_without_token(self):
        response = self.client.get(f"{self.url}pending_events/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    
    def test_incorrect_get_pending_events_normal_user(self):
        token = self.login(self.user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(f"{self.url}pending_events/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
