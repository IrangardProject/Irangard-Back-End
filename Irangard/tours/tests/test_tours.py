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


# class TourViewSetTestCase(TestCase):

#     def login(self, username, password):
#         url = reverse('accounts:accounts-jwt-create')
#         data = json.dumps({'username': username, 'password': password})
#         response = self.client.post(url, data, content_type='application/json')
#         if response.status_code == status.HTTP_200_OK:
#             access_token = response.data['access']
#             return access_token
#         else:
#             return "incorrect"

#     def setUp(self):
#         self.user = User.objects.create(
#             email="emad12@gmail.com",
#             username="emad12",
#             first_name="سید عماد",
#             last_name="موسوی",
#             phone_no="09364945328"
#         )
#         self.user.set_password('emad1234')
#         self.user.is_special = True
#         self.user.save()

#         self.special_user = SpecialUser.objects.create(
#             user=self.user, total_revenue=0)
#         self.special_user.save()

#         self.url = 'http://127.0.0.1/tours/'
#         self.client = APIClient()
#         token = self.login(self.special_user.user.username, 'emad1234')
#         self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

#         self.data = {
#             "title": "test_tour",
#             "cost": 200,
#             "capacity": 50,
#             "remaining": 50,
#             "start_date": "2022-05-22T15:49:49.505Z",
#             "end_date": "2022-05-23T15:49:49.505Z"
#         }

#     def normal_user_client(self):
#         user = User.objects.create(
#             email="emad@gmail.com",
#             username="emad",
#             first_name="سید عماد",
#             last_name="موسوی",
#             phone_no="09364945328"
#         )
#         user.set_password('emad12345')
#         user.is_special = True
#         user.save()

#         client = APIClient()
#         token = self.login(user.username, 'emad12345')
#         client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

#         return client

#     @classmethod
#     def setUpTestData(cls):
#         return super().setUpTestData()

#     def test_tour_create(self):

#         response = self.client.post(self.url, json.dumps(
#             self.data, indent=4, sort_keys=True, default=str), content_type='application/json')

#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_tour_create_not_superuser(self):
        
#         client = self.normal_user_client()
#         response = client.post(self.url, json.dumps(
#             self.data, indent=4, sort_keys=True, default=str), content_type='application/json')

#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     def test_tour_create_not_given_title(self):

#         data = self.data
#         data.pop('title')
#         response = self.client.post(self.url, json.dumps(
#             data, indent=4, sort_keys=True, default=str), content_type='application/json')

#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_tour_create_not_given_cost(self):
#         data = self.data
#         data.pop('cost')
#         client = self.normal_user_client()
#         response = client.post(self.url, json.dumps(
#             data, indent=4, sort_keys=True, default=str), content_type='application/json')

#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_tour_create_not_given_capacity(self):
#         data = self.data
#         data.pop('capacity')
#         client = self.normal_user_client()
#         response = client.post(self.url, json.dumps(
#             data, indent=4, sort_keys=True, default=str), content_type='application/json')

#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_tour_create_not_given_start_date(self):
#         data = self.data
#         data.pop('start_date')
#         client = self.normal_user_client()
#         response = client.post(self.url, json.dumps(
#             data, indent=4, sort_keys=True, default=str), content_type='application/json')

#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_tour_create_not_given_end_date(self):
#         data = self.data
#         data.pop('end_date')
#         client = self.normal_user_client()
#         response = client.post(self.url, json.dumps(
#             data, indent=4, sort_keys=True, default=str), content_type='application/json')

#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_tour_create_not_given_remaining(self):
#         data = self.data
#         data.pop('remaining')
#         client = self.normal_user_client()
#         response = client.post(self.url, json.dumps(
#             data, indent=4, sort_keys=True, default=str), content_type='application/json')

#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_tour_update(self):
#         pass

#     def test_tour_partial_update(self):
#         pass

#     def test_tour_update_not_owner(self):
#         pass

#     def test_tour_delete(self):
#         pass

#     def test_tour_delete_not_owner(self):
#         pass

#     def test_tour_book(self):
#         pass

#     def test_tour_book_not_authenticated(self):
#         pass

#     def test_tour_verify(self):
#         pass
