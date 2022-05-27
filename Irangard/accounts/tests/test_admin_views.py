from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django import urls
import json
from django.http import HttpRequest
from rest_framework import permissions, status
from rest_framework.response import Response
from ..models import *
from django.urls import reverse
import mock


# class AdminViewSetTestCase(TestCase):
#     def setUp(self):

#         self.admin = User.objects.create(
#             email="admin@gmail.com",
#             username="admin",
#             first_name="سید عماد",
#             last_name="موسوی",
#             phone_no="09364945328",
#             is_admin=True
#         )
#         self.admin.set_password('admin')
#         self.admin.save()
#         self.client = APIClient
#         self.client.force_authenticate(user=self.admin)

#     @classmethod
#     def setUpTestData(cls):
#         return super().setUpTestData()

#     def test_addAdmin(self):

#         url = reverse('accounts:accounts-admin-add-admin')
#         response = self.client.post(path=url,content_type='application/json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_removeSpecialUser(self):

#         url = reverse('accounts:accounts-admin-remove-special-user')
#         response = self.client.post(path=url,content_type='application/json')

#     def test_removeUser(self, mocked_ActivationEmail):

#         url = reverse('accounts:accounts-admin-remove-user')
#         response = self.client.post(path=url,content_type='application/json')

#     def test_addUser(self):
#         url = reverse('accounts:accounts-admin-add-user')
#         response = self.client.post(path=url,content_type='application/json')
