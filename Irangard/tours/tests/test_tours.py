import json
import datetime
import mock
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.http import HttpRequest
from rest_framework import permissions, status
from rest_framework.response import Response
from ..models import *
from accounts.models import User, SpecialUser


class TourViewSetTestCase(TestCase):

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
        
        #create main super-user
        self.user = User.objects.create(
            email="emad12@gmail.com",
            username="emad12",
            first_name="سید عماد",
            last_name="موسوی",
            phone_no="09364945328"
        )
        self.user.set_password('emad1234')
        self.user.is_special = True
        self.user.save()

        self.special_user = SpecialUser.objects.create(
            user=self.user, total_revenue=0)
        self.special_user.save()
        #end create main super-user
        
        #create second super-user
        self.second_user = User.objects.create(
            email="emad13@gmail.com",
            username="emad13",
            first_name="سید عماد",
            last_name="موسوی",
            phone_no="09364945328"
        )
        self.second_user.set_password('emad123456')
        self.second_user.is_special = True
        self.second_user.save()

        self.second_special_user = SpecialUser.objects.create(
            user=self.second_user, total_revenue=0)
        self.second_special_user.save()
        #end create second super-user
        self.url = 'http://127.0.0.1:8000/tours/'
        self.client = APIClient()
        token = self.login(self.special_user.user.username, 'emad1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        self.data = {
            "title": "test_tour",
            "cost": 200,
            "capacity": 50,
            "remaining": 50,
            "start_date": "2022-05-22T15:49:49.505Z",
            "end_date": "2022-05-23T15:49:49.505Z",
            "tour_type": "0"
        }
        
        self.data_1 ={
            "title": "test_tour",
            "cost": 200,
            "capacity": 50,
            "remaining": 50,
            "start_date": "2022-05-22T15:49:49.505Z",
            "end_date": "2022-05-23T15:49:49.505Z",
            "tour_type": "1"
        }

        self.tour = Tour.objects.create(**self.data, owner=self.special_user)
        self.tour1 = Tour.objects.create(**self.data_1, owner=self.special_user)
        self.tour2 = Tour.objects.create(**self.data_1, owner=self.special_user)
        self.tour.save()
        self.tour1.save()
        self.tour2.save()
        
        
    def normal_user_client(self):
        user = User.objects.create(
            email="emad@gmail.com",
            username="emad",
            first_name="سید عماد",
            last_name="موسوی",
            phone_no="09364945328"
        )
        user.set_password('emad12345')
        user.save()

        client = APIClient()
        token = self.login(user.username, 'emad12345')
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        return client

    @classmethod
    def setUpTestData(cls):
        return super().setUpTestData()

    def test_tour_create(self):

        response = self.client.post(self.url, json.dumps(
            self.data, indent=4, sort_keys=True, default=str), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_tour_create_incorrect(self):

        response = self.client.post(self.url + "HelloTest", json.dumps(
            self.data, indent=4, sort_keys=True, default=str), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_301_MOVED_PERMANENTLY)

    def test_tour_create_not_superuser(self):

        client = self.normal_user_client()
        response = client.post(self.url, json.dumps(
            self.data, indent=4, sort_keys=True, default=str), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_tour_create_not_given_title(self):

        data = self.data.copy()
        data.pop('title')
        response = self.client.post(self.url, json.dumps(
            data, indent=4, sort_keys=True, default=str), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_tour_create_not_given_start_date(self):
        data = self.data.copy()
        data.pop('start_date')
        response = self.client.post(self.url, json.dumps(
            data, indent=4, sort_keys=True, default=str), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_tour_create_not_given_end_date(self):
        data = self.data.copy()
        data.pop('end_date')
        response = self.client.post(self.url, json.dumps(
            data, indent=4, sort_keys=True, default=str), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_tour_update(self):
        data = self.data.copy()
        data['title'] = 'test_title'
        data['cost'] = 100
        response = self.client.put(self.url + f'{self.tour.id}/', json.dumps(
            data, indent=4, sort_keys=True, default=str), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_tour_update_incorrect_url(self):
        data = self.data.copy()
        data['title'] = 'test_title'
        data['cost'] = 100
        response = self.client.put(self.url + "bug" + f'{self.tour.id}/', json.dumps(
            data, indent=4, sort_keys=True, default=str), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_tour_partial_update(self):
        data = {"title":"test_title"}
        response = self.client.put(self.url + f'{self.tour.id}/', json.dumps(
            data, indent=4, sort_keys=True, default=str), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_tour_update_not_owner(self):
        data = {"title":"test_title"}
        client = APIClient()
        client.login(username=self.second_special_user.user.username, password='emad123456')
        response = client.put(self.url + f'{self.tour.id}/', json.dumps(
            data, indent=4, sort_keys=True, default=str), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_tour_update_incorrect_credentials(self):
        data = {"title":"test_title"}
        client = APIClient()
        client.login(username=self.second_special_user.user.username, password='emad12345678')
        response = client.put(self.url + f'{self.tour.id}/', json.dumps(
            data, indent=4, sort_keys=True, default=str), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_tour_delete(self):
        response = self.client.delete(self.url + f'{self.tour.id}/', json.dumps(
            self.data, indent=4, sort_keys=True, default=str), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_tour_delete_not_owner(self):
        data = {"title":"test_title"}
        client = APIClient()
        client.login(username=self.second_special_user.user.username, password='emad123456')
        response = client.delete(self.url + f'{self.tour.id}/', json.dumps(
            data, indent=4, sort_keys=True, default=str), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_tour_delete_incorrect_credentials(self):
        data = {"title":"test_title"}
        client = APIClient()
        client.login(username=self.second_special_user.user.username, password='emad12345678')
        response = client.delete(self.url + f'{self.tour.id}/', json.dumps(
            data, indent=4, sort_keys=True, default=str), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_tour_delete_incorrect_url(self):
        data = {"title":"test_title"}
        client = APIClient()
        client.login(username=self.second_special_user.user.username, password='emad123456')
        response = client.delete(self.url + '2050/', json.dumps(
            data, indent=4, sort_keys=True, default=str), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    
    def test_tour_type_filter(self):
        response = self.client.get(self.url + '?tour_type=1')
        response_dict = json.loads(response.content)
        tour_list = response_dict['results']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for tour in tour_list:
            self.assertEqual(tour["tour_type"], "1")
        

    def test_tour_book(self):
        pass

    def test_tour_book_not_authenticated(self):
        pass

    def test_tour_verify(self):
        pass
