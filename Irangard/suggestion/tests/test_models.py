from django.test import TestCase
from ..models import TourSuggestion, EventSuggestion, PlaceSuggestion
from accounts.models import User, SpecialUser
from tours.models import Tour
from events.models import Event
from places.models import Place

    
class BaseTestCase(TestCase):
    
    def make_user(self, username, email, password):
        user = User.objects.create_user(username, email, password)
        return user


class TourSuggestionTestCase(BaseTestCase):
     
    def make_tour(self):
        self.special_user = SpecialUser.objects.create(
            user=self.user, total_revenue=0)
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
    
    
    def setUp(self):
        self.user = self.make_user('creator', 'creator@gmail.com', '123456')
        self.user1 = self.make_user('amir', 'amir@gmail.com', '123456')
        self.user2 = self.make_user('amin', 'amin@gmail.com', '123456')
        self.tour = self.make_tour()
        tour_suggestion = TourSuggestion.objects.create(
            sender=self.user1, 
            receiver=self.user2, 
            tour=self.tour, 
            text="test")
        self.obj_pk = tour_suggestion.pk

        
    def test_sender(self):
        suggestion = TourSuggestion.objects.get(pk=self.obj_pk)
        self.assertEqual(suggestion.sender, self.user1)
        
    
    def test_receiver(self):
        suggestion = TourSuggestion.objects.get(pk=self.obj_pk)
        self.assertEqual(suggestion.receiver, self.user2)
        
    
    def test_tour(self):
        suggestion = TourSuggestion.objects.get(pk=self.obj_pk)
        self.assertEqual(suggestion.tour, self.tour)
    
    
    def test_text(self):
        suggestion = TourSuggestion.objects.get(pk=self.obj_pk)
        self.assertEqual(suggestion.text, "test")
    

class EventSuggestionTestCase(BaseTestCase):
    
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

    
    def setUp(self):
        self.user = self.make_user('creator', 'creator@gmail.com', '123456')
        self.user1 = self.make_user('amir', 'amir@gmail.com', '123456')
        self.user2 = self.make_user('amin', 'amin@gmail.com', '123456')
        self.event = self.make_event()
        event_suggestion = EventSuggestion.objects.create(
            sender=self.user1, 
            receiver=self.user2, 
            event=self.event, 
            text="test"
        )
        self.obj_pk = event_suggestion.pk

    
    def test_sender(self):
        suggestion = EventSuggestion.objects.get(pk=self.obj_pk)
        self.assertEqual(suggestion.sender, self.user1)
        
    
    def test_receiver(self):
        suggestion = EventSuggestion.objects.get(pk=self.obj_pk)
        self.assertEqual(suggestion.receiver, self.user2)
        
    
    def test_event(self):
        suggestion = EventSuggestion.objects.get(pk=self.obj_pk)
        self.assertEqual(suggestion.event, self.event)
    
    
    def test_text(self):
        suggestion = EventSuggestion.objects.get(pk=self.obj_pk)
        self.assertEqual(suggestion.text, "test")


class PlaceSuggestionTestCase(BaseTestCase):
    
    def make_place(self):
        place = Place.objects.create(
            place_type=1, title="test place", 
            description="test description", added_by=self.user)
        return place
    
    
    def setUp(self):
        self.user = self.make_user('creator', 'creator@gmail.com', '123456')
        self.user1 = self.make_user('amir', 'amir@gmail.com', '123456')
        self.user2 = self.make_user('amin', 'amin@gmail.com', '123456')
        self.place = self.make_place()
        place_suggestion = PlaceSuggestion.objects.create(
            sender=self.user1, 
            receiver=self.user2, 
            place=self.place, 
            text="test")
        self.obj_pk = place_suggestion.pk
        
    
    def test_sender(self):
        suggestion = PlaceSuggestion.objects.get(pk=self.obj_pk)
        self.assertEqual(suggestion.sender, self.user1)
        
    
    def test_receiver(self):
        suggestion = PlaceSuggestion.objects.get(pk=self.obj_pk)
        self.assertEqual(suggestion.receiver, self.user2)
        
    
    def test_place(self):
        suggestion = PlaceSuggestion.objects.get(pk=self.obj_pk)
        self.assertEqual(suggestion.place, self.place)
    
    
    def test_text(self):
        suggestion = PlaceSuggestion.objects.get(pk=self.obj_pk)
        self.assertEqual(suggestion.text, "test")
        