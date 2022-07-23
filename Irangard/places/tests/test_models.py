from django.test import TestCase
from ..models import *
from django.urls import reverse
import json
from rest_framework import status
from rest_framework.test import APIClient


class PlaceTestCase(TestCase):

    def make_user(self):
        self.user = User.objects.create(username="ghazal", email="ghazal@gmail.com")
        self.user.set_password("gh1234")
        self.user.save()
        return self.user

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
    
    def setUp(self):
        self.client = APIClient()
        self.user = self.make_user()
        token = self.login(self.user.username, self.user.password)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        Place.objects.create(
            place_type=1, title="test place", description="test description", added_by=self.user)
        
    def test_title(self):
        place = Place.objects.get(title="test place")
        self.assertEqual(place.title, "test place")
        
    def test_user(self):
        place = Place.objects.get(title="test place")
        self.assertEqual(place.added_by, self.user)

    def test_description(self):
        place = Place.objects.get(title="test place")
        self.assertEqual(place.description, "test description")

    def test_place_type(self):
        place = Place.objects.get(title="test place")
        self.assertEqual(place.place_type, '1')


class ContactTestCase(TestCase):

    def make_user(self):
        self.user = User.objects.create(username="ghazal", email="ghazal@gmail.com")
        self.user.set_password("gh1234")
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
        self.place = Place.objects.create(
            place_type=1, title="test place", description="test description", added_by=self.user)
        Contact.objects.create(
            place=self.place, x_location=0, y_location=0, province="test province", city="test city")
        
    def test_x_location(self):
        contact = Contact.objects.get(place=self.place)
        self.assertEqual(contact.x_location, 0)
        
    def test_x_location(self):
        contact = Contact.objects.get(place=self.place)
        self.assertEqual(contact.x_location, 0)

    def test_y_location(self):
        contact = Contact.objects.get(place=self.place)
        self.assertEqual(contact.y_location, 0)

    def test_province(self):
        contact = Contact.objects.get(place=self.place)
        self.assertEqual(contact.province, "test province")

    def test_city(self):
        contact = Contact.objects.get(place=self.place)
        self.assertEqual(contact.city, "test city")


class TagTestCase(TestCase):

    def make_user(self):
        self.user = User.objects.create(username="ghazal", email="ghazal@gmail.com")
        self.user.set_password("gh1234")
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
        self.place = Place.objects.create(
            place_type=1, title="test place", description="test description", added_by=self.user)
        Tag.objects.create(place=self.place, name="test tag")
        
    def test_name(self):
        tag = Tag.objects.get(place=self.place)
        self.assertEqual(tag.name, "test tag")


class FeatureTestCase(TestCase):

    def make_user(self):
        self.user = User.objects.create(username="ghazal", email="ghazal@gmail.com")
        self.user.set_password("gh1234")
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
        self.place = Place.objects.create(
            place_type=1, title="test place", description="test description", added_by=self.user)
        Feature.objects.create(place=self.place, title="test feature")
        
    def test_feature(self):
        feature = Feature.objects.get(place=self.place)
        self.assertEqual(feature.title, "test feature")



class RoomTestCase(TestCase):

    def make_user(self):
        self.user = User.objects.create(username="ghazal", email="ghazal@gmail.com")
        self.user.set_password("gh1234")
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
        self.place = Place.objects.create(
            place_type=1, title="test place", description="test description", added_by=self.user)
        Room.objects.create(
            place=self.place, room_type="test room type", capacity=2, price=50000)
        
    def test_room_type(self):
        room = Room.objects.get(place=self.place)
        self.assertEqual(room.room_type, "test room type")

    def test_capacity(self):
        room = Room.objects.get(place=self.place)
        self.assertEqual(room.capacity, 2)

    def test_price(self):
        room = Room.objects.get(place=self.place)
        self.assertEqual(room.price, 50000)


class OptionalTestCase(TestCase):

    def make_user(self):
        self.user = User.objects.create(username="ghazal", email="ghazal@gmail.com")
        self.user.set_password("gh1234")
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
        self.place = Place.objects.create(
            place_type=1, title="test place", description="test description", added_by=self.user)
        Optional.objects.create(
            place=self.place, title="test title", description="test description", price=40000)
        
    def test_title(self):
        optional = Optional.objects.get(place=self.place)
        self.assertEqual(optional.title, "test title")

    def test_description(self):
        optional = Optional.objects.get(place=self.place)
        self.assertEqual(optional.description, "test description")

    def test_price(self):
        optional = Optional.objects.get(place=self.place)
        self.assertEqual(optional.price, 40000)
