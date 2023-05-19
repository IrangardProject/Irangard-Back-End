from django.test import TestCase
from ..models import TourSuggestion, EventSuggestion, PlaceSuggestion
from accounts.models import User, SpecialUser
from tours.models import Tour
from events.models import Event
from places.models import Place
from rest_framework.test import APIClient
from django.urls import reverse
import json
from rest_framework import status
import json


class BaseTestCase(TestCase):
    
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


    def make_event(self):
        event = Event.objects.create(
            event_type='0', event_category='0', title='test event', 
            organizer='test organizer', description='test description', 
            x_location=0, y_location=0, start_date='2022-05-22', 
            end_date='2022-05-23', start_time='00:00:00', end_time='00:00:00',
            added_by=self.user, address='test address', is_free=True,
            province='تهران', city='تهران', website='www.org.com', 
            phone='09109530195')
        return event

    
    def make_place(self):
        place = Place.objects.create(
            place_type=1, title="test place", 
            description="test description", added_by=self.user)
        return place
    

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
        self.url_tour = 'http://127.0.0.1:8000/suggestion/tour/'
        self.url_event = 'http://127.0.0.1:8000/suggestion/event/'
        self.url_place = 'http://127.0.0.1:8000/suggestion/place/'
        
        self.user = self.make_user('amir', '123456', 'amir@gmail.com')
        self.special_user = SpecialUser.objects.create(
            user=self.user, total_revenue=0)
        self.user1 = self.make_user('ali', '123456','ali@gmail.com')
        self.user2 = self.make_user('amin', '123456', 'amin@gmail.com')
        self.user3 = self.make_user('armin', '123456', 'armin@gmail.com')
        self.cheater_user = self.make_user("cheater", "123456", "cheater@gmail.com")
        
        self.super_user = self.make_super_user("superuser", "123456", "super@gmail.com")
        self.tour = self.make_tour()
        self.event = self.make_event()
        self.place = self.make_place()
        
        self.place_suggestion = PlaceSuggestion.objects.create(
            sender=self.user1, 
            receiver=self.user2, 
            place=self.place, 
            text="test")
        
        self.event_suggestion = EventSuggestion.objects.create(
            sender=self.user1, 
            receiver=self.user2, 
            event=self.event, 
            text="test"
        )
        
        self.tour_suggestion = TourSuggestion.objects.create(
            sender=self.user1, 
            receiver=self.user2, 
            tour=self.tour, 
            text="test"
        )
        
        self.place_suggestion2 = PlaceSuggestion.objects.create(
            sender=self.user2, 
            receiver=self.user1, 
            place=self.place, 
            text="test")
        
        self.event_suggestion2 = EventSuggestion.objects.create(
            sender=self.user2, 
            receiver=self.user1, 
            event=self.event, 
            text="test"
        )
        
        self.tour_suggestion3 = TourSuggestion.objects.create(
            sender=self.user2, 
            receiver=self.user1, 
            tour=self.tour, 
            text="test"
        )
 

class TourSuggestionViewsTestCase(BaseTestCase):
    
    def test_correct_get_tour_suggestions_super_user(self):
        token = self.login(self.super_user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(self.url_tour)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
          
    
    def test_incorrect_get_tour_suggestions_normal_user(self):
        token = self.login(self.user1.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(self.url_tour)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    
    def test_correct_retrieve_tour_suggestion_sender_user(self):
        token = self.login(self.user1.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(self.url_tour + str(self.tour_suggestion.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
    def test_correct_retrieve_tour_suggestion_receiver_user(self):
        token = self.login(self.user2.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(self.url_tour + str(self.tour_suggestion.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    
    def test_correct_retrieve_tour_suggestion_super_user(self):
        token = self.login(self.super_user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(self.url_tour + str(self.tour_suggestion.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
    def test_incorrect_retrieve_tour_suggestion_cheater_user(self):
        token = self.login(self.cheater_user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(self.url_tour + str(self.tour_suggestion.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    
    def test_correct_post_tour_suggestion(self):
        token = self.login(self.user2.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            "receiver": self.user3.pk,
            "text": "test",
            "tour": self.tour.pk
        }
        response = self.client.post(self.url_tour, data=data)
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
        response = self.client.post(self.url_tour, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    
    def test_incorrect_post_without_token(self):
        data = {
            "receiver": self.user3.pk,
            "text": "test",
            "tour": self.tour.pk
        }
        response = self.client.post(self.url_tour, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    
    def test_incorrect_post_repetitive_sender_receiver_tour(self):
        token = self.login(self.user1.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            "receiver": self.user2.pk,
            "text": "test",
            "tour": self.tour.pk
        }
        response = self.client.post(self.url_tour, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    
    def test_incorrect_post_same_sender_receiver(self):
        token = self.login(self.user1.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            "receiver": self.user1.pk,
            "text": "test",
            "tour": self.tour.pk
        }
        response = self.client.post(self.url_tour, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    
    def test_correct_put_sender_user_token(self):
        token = self.login(self.user1.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            "text": "updated text"
        }
        response = self.client.put(self.url_tour + str(self.tour_suggestion.pk) + '/', data=data)
        self.tour_suggestion.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.tour_suggestion.text, "updated text")
        
    
    def test_correct_put_super_user_token(self):
        token = self.login(self.super_user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            "text": "updated text"
        }
        response = self.client.put(self.url_tour + str(self.tour_suggestion.pk) + '/', data=data)
        self.tour_suggestion.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.tour_suggestion.text, "updated text")
        
    
    def test_incorrect_put_receiver_field_included(self):
        token = self.login(self.user1.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            "receiver": self.user3.pk,
            "text": "updated text"
        }
        response = self.client.put(self.url_tour + str(self.tour_suggestion.pk) + '/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    
    def test_incorrect_put_tour_field_included(self):
        token = self.login(self.user1.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            "tour": self.tour.pk,
            "text": "updated text"
        }
        response = self.client.put(self.url_tour + str(self.tour_suggestion.pk) + '/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    
    def test_incorrect_put_without_token(self):
        data = {
            "text": "updated text"
        }
        response = self.client.put(self.url_tour + str(self.tour_suggestion.pk) + '/', data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    
    def test_incorrect_put_receiver_user_token(self):
        token = self.login(self.user2.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            "text": "updated text"
        }
        response = self.client.put(self.url_tour + str(self.tour_suggestion.pk) + '/', data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    
    def test_incorrect_put_cheater_user_token(self):
        token = self.login(self.cheater_user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            "text": "updated text"
        }
        response = self.client.put(self.url_tour + str(self.tour_suggestion.pk) + '/', data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    
    def test_correct_delete_sender_user_token(self):
        token = self.login(self.user1.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.delete(self.url_tour + str(self.tour_suggestion.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    
    def test_correct_delete_super_user_token(self):
        token = self.login(self.super_user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.delete(self.url_tour + str(self.tour_suggestion.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    
    def test_incorrect_delete_without_token(self):
        response = self.client.delete(self.url_tour + str(self.tour_suggestion.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    
    def test_correct_delete_receiver_user_token(self):
        token = self.login(self.user2.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.delete(self.url_tour + str(self.tour_suggestion.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    
    def test_incorrect_delete_cheater_user_token(self):
        token = self.login(self.cheater_user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.delete(self.url_tour + str(self.tour_suggestion.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    
    def test_correct_get_sender_suggestions(self):
        token = self.login(self.user1.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(self.url_tour + 'sender_suggestions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for es in response.data:
            self.assertEqual(es['sender'], self.user1.pk)
    
    
    def test_incorrect_get_sender_suggestions_without_token(self):
        response = self.client.get(self.url_tour + 'sender_suggestions/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    
    def test_correct_get_receiver_suggestions(self):
        token = self.login(self.user2.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(self.url_tour + 'receiver_suggestions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for es in response.data:
            self.assertEqual(es['receiver'], self.user2.pk)
    
    
    def test_incorrect_get_receiver_suggestions_without_token(self):
        response = self.client.get(self.url_tour + 'receiver_suggestions/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)   
    

class EventSuggestionViewsTestCase(BaseTestCase):
    
    def test_correct_get_event_suggestions_super_user(self):
        token = self.login(self.super_user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(self.url_event)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
          
    
    def test_incorrect_get_event_suggestions_normal_user(self):
        token = self.login(self.user1.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(self.url_event)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    
    def test_correct_retrieve_event_suggestion_sender_user(self):
        token = self.login(self.user1.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(self.url_event + str(self.event_suggestion.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
    def test_correct_retrieve_event_suggestion_receiver_user(self):
        token = self.login(self.user2.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(self.url_event + str(self.event_suggestion.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    
    def test_correct_retrieve_event_suggestion_super_user(self):
        token = self.login(self.super_user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(self.url_event + str(self.event_suggestion.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
    def test_incorrect_retrieve_event_suggestion_cheater_user(self):
        token = self.login(self.cheater_user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(self.url_event + str(self.event_suggestion.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    
    def test_correct_post_event_suggestion(self):
        token = self.login(self.user2.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            "receiver": self.user3.pk,
            "text": "test",
            "event": self.event.pk
        }
        response = self.client.post(self.url_event, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    
    def test_correct_post_event_suggestion_ignore_sender_field(self):
        token = self.login(self.user2.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            "sender": 10000,
            "receiver": self.user3.pk,
            "text": "test",
            "event": self.event.pk
        }
        response = self.client.post(self.url_event, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    
    def test_incorrect_post_without_token(self):
        data = {
            "receiver": self.user3.pk,
            "text": "test",
            "event": self.event.pk
        }
        response = self.client.post(self.url_event, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    
    def test_incorrect_post_repetitive_sender_receiver_event(self):
        token = self.login(self.user1.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            "receiver": self.user2.pk,
            "text": "test",
            "event": self.event.pk
        }
        response = self.client.post(self.url_event, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    
    def test_incorrect_post_same_sender_receiver(self):
        token = self.login(self.user1.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            "receiver": self.user1.pk,
            "text": "test",
            "event": self.event.pk
        }
        response = self.client.post(self.url_event, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    
    def test_correct_put_sender_user_token(self):
        token = self.login(self.user1.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            "text": "updated text"
        }
        response = self.client.put(self.url_event + str(self.event_suggestion.pk) + '/', data=data)
        self.event_suggestion.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.event_suggestion.text, "updated text")
        
    
    def test_correct_put_super_user_token(self):
        token = self.login(self.super_user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            "text": "updated text"
        }
        response = self.client.put(self.url_event + str(self.event_suggestion.pk) + '/', data=data)
        self.event_suggestion.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.event_suggestion.text, "updated text")
        
    
    def test_incorrect_put_receiver_field_included(self):
        token = self.login(self.user1.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            "receiver": self.user3.pk,
            "text": "updated text"
        }
        response = self.client.put(self.url_event + str(self.event_suggestion.pk) + '/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    
    def test_incorrect_put_event_field_included(self):
        token = self.login(self.user1.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            "event": self.event.pk,
            "text": "updated text"
        }
        response = self.client.put(self.url_event + str(self.event_suggestion.pk) + '/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    
    def test_incorrect_put_without_token(self):
        data = {
            "text": "updated text"
        }
        response = self.client.put(self.url_event + str(self.event_suggestion.pk) + '/', data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    
    def test_incorrect_put_receiver_user_token(self):
        token = self.login(self.user2.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            "text": "updated text"
        }
        response = self.client.put(self.url_event + str(self.event_suggestion.pk) + '/', data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    
    def test_incorrect_put_cheater_user_token(self):
        token = self.login(self.cheater_user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            "text": "updated text"
        }
        response = self.client.put(self.url_event + str(self.event_suggestion.pk) + '/', data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    
    def test_correct_delete_sender_user_token(self):
        token = self.login(self.user1.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.delete(self.url_event + str(self.event_suggestion.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    
    def test_correct_delete_super_user_token(self):
        token = self.login(self.super_user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.delete(self.url_event + str(self.event_suggestion.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    
    def test_incorrect_delete_without_token(self):
        response = self.client.delete(self.url_event + str(self.event_suggestion.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    
    def test_correct_delete_receiver_user_token(self):
        token = self.login(self.user2.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.delete(self.url_event + str(self.event_suggestion.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    
    def test_incorrect_delete_cheater_user_token(self):
        token = self.login(self.cheater_user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.delete(self.url_event + str(self.event_suggestion.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    
    def test_correct_get_sender_suggestions(self):
        token = self.login(self.user1.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(self.url_event + 'sender_suggestions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for es in response.data:
            self.assertEqual(es['sender'], self.user1.pk)
    
    
    def test_incorrect_get_sender_suggestions_without_token(self):
        response = self.client.get(self.url_event + 'sender_suggestions/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    
    def test_correct_get_receiver_suggestions(self):
        token = self.login(self.user2.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(self.url_event + 'receiver_suggestions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for es in response.data:
            self.assertEqual(es['receiver'], self.user2.pk)
    
    
    def test_incorrect_get_receiver_suggestions_without_token(self):
        response = self.client.get(self.url_event + 'receiver_suggestions/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

 
class placeSuggestionViewsTestCase(BaseTestCase):
    
    def test_correct_get_place_suggestions_super_user(self):
        token = self.login(self.super_user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(self.url_place)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
          
    
    def test_incorrect_get_place_suggestions_normal_user(self):
        token = self.login(self.user1.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(self.url_place)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    
    def test_correct_retrieve_place_suggestion_sender_user(self):
        token = self.login(self.user1.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(self.url_place + str(self.place_suggestion.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
    def test_correct_retrieve_place_suggestion_receiver_user(self):
        token = self.login(self.user2.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(self.url_place + str(self.place_suggestion.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    
    def test_correct_retrieve_place_suggestion_super_user(self):
        token = self.login(self.super_user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(self.url_place + str(self.place_suggestion.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
    def test_incorrect_retrieve_place_suggestion_cheater_user(self):
        token = self.login(self.cheater_user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(self.url_place + str(self.place_suggestion.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    
    def test_correct_post_place_suggestion(self):
        token = self.login(self.user2.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            "receiver": self.user3.pk,
            "text": "test",
            "place": self.place.pk
        }
        response = self.client.post(self.url_place, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    
    def test_correct_post_place_suggestion_ignore_sender_field(self):
        token = self.login(self.user2.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            "sender": 10000,
            "receiver": self.user3.pk,
            "text": "test",
            "place": self.place.pk
        }
        response = self.client.post(self.url_place, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    
    def test_incorrect_post_without_token(self):
        data = {
            "receiver": self.user3.pk,
            "text": "test",
            "place": self.place.pk
        }
        response = self.client.post(self.url_place, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    
    def test_incorrect_post_repetitive_sender_receiver_place(self):
        token = self.login(self.user1.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            "receiver": self.user2.pk,
            "text": "test",
            "place": self.place.pk
        }
        response = self.client.post(self.url_place, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    
    def test_incorrect_post_same_sender_receiver(self):
        token = self.login(self.user1.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            "receiver": self.user1.pk,
            "text": "test",
            "place": self.place.pk
        }
        response = self.client.post(self.url_place, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    
    def test_correct_put_sender_user_token(self):
        token = self.login(self.user1.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            "text": "updated text"
        }
        response = self.client.put(self.url_place + str(self.place_suggestion.pk) + '/', data=data)
        self.place_suggestion.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.place_suggestion.text, "updated text")
        
    
    def test_correct_put_super_user_token(self):
        token = self.login(self.super_user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            "text": "updated text"
        }
        response = self.client.put(self.url_place + str(self.place_suggestion.pk) + '/', data=data)
        self.place_suggestion.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.place_suggestion.text, "updated text")
        
    
    def test_incorrect_put_receiver_field_included(self):
        token = self.login(self.user1.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            "receiver": self.user3.pk,
            "text": "updated text"
        }
        response = self.client.put(self.url_place + str(self.place_suggestion.pk) + '/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    
    def test_incorrect_put_place_field_included(self):
        token = self.login(self.user1.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            "place": self.place.pk,
            "text": "updated text"
        }
        response = self.client.put(self.url_place + str(self.place_suggestion.pk) + '/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    
    def test_incorrect_put_without_token(self):
        data = {
            "text": "updated text"
        }
        response = self.client.put(self.url_place + str(self.place_suggestion.pk) + '/', data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    
    def test_incorrect_put_receiver_user_token(self):
        token = self.login(self.user2.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            "text": "updated text"
        }
        response = self.client.put(self.url_place + str(self.place_suggestion.pk) + '/', data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    
    def test_incorrect_put_cheater_user_token(self):
        token = self.login(self.cheater_user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            "text": "updated text"
        }
        response = self.client.put(self.url_place + str(self.place_suggestion.pk) + '/', data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    
    def test_correct_delete_sender_user_token(self):
        token = self.login(self.user1.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.delete(self.url_place + str(self.place_suggestion.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    
    def test_correct_delete_super_user_token(self):
        token = self.login(self.super_user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.delete(self.url_place + str(self.place_suggestion.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    
    def test_incorrect_delete_without_token(self):
        response = self.client.delete(self.url_place + str(self.place_suggestion.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    
    def test_correct_delete_receiver_user_token(self):
        token = self.login(self.user2.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.delete(self.url_place + str(self.place_suggestion.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    
    def test_incorrect_delete_cheater_user_token(self):
        token = self.login(self.cheater_user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.delete(self.url_place + str(self.place_suggestion.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        
    def test_correct_get_sender_suggestions(self):
        token = self.login(self.user1.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(self.url_place + 'sender_suggestions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for es in response.data:
            self.assertEqual(es['sender'], self.user1.pk)
    
    
    def test_incorrect_get_sender_suggestions_without_token(self):
        response = self.client.get(self.url_place + 'sender_suggestions/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    
    def test_correct_get_receiver_suggestions(self):
        token = self.login(self.user2.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(self.url_place + 'receiver_suggestions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for es in response.data:
            self.assertEqual(es['receiver'], self.user2.pk)
    
    
    def test_incorrect_get_receiver_suggestions_without_token(self):
        response = self.client.get(self.url_place + 'receiver_suggestions/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
