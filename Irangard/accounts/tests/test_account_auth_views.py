from django.test import TestCase, Client
from rest_framework import status
from django import urls
import json
from django.http import HttpRequest
from rest_framework import permissions, status
from rest_framework.response import Response
from ..models import *
import mock


class AccountAuthViewSetTestCase(TestCase):
    def setUp(self):

        User.objects.create(
            email="emad@gmail.com",
            username="Emad",
            first_name="سید عماد",
            last_name="موسوی",
            phone_no="09364945328",
            password='123456',
        )

        self.verification_obj = Verification.objects.create(
            email='admin@gmail.com',
            username='admin',
            token='4321'
        )

        self.viewset_url = 'http://127.0.0.1:8000/accounts/auth/'

    @classmethod
    def setUpTestData(cls):
        return super().setUpTestData()

    def test_check_email(self):

        # response should be 400 because email already exists
        response = self.client.post(
            path=self.viewset_url + 'check-email/',
            data={
                'email': 'emad@gmail.com'
            })
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

        # response should be 200 because email doesn't exist
        response = self.client.post(
            path=self.viewset_url + 'check-email/',
            data={
                'email': 'new@gmail.com'
            })
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_check_username(self):

        # response should be 00 because username already exists
        response = self.client.post(
            path=self.viewset_url + 'check-username/',
            data={
                'username': 'Emad'
            })
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

        # response should be 00 because username doesn't exist
        response = self.client.post(
            path=self.viewset_url + 'check-username/',
            data={
                'username': 'new-username'
            })
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    @mock.patch('accounts.accounts_auth_views.AccountAuthViewSet.ActivationEmail',
                return_value=Response(status=status.HTTP_200_OK, data='Email sent successfully'))
    def test_activate(self, mocked_ActivationEmail):

        # response should be 400 because username already exists
        response = self.client.post(
            path=self.viewset_url + 'activate/',
            data={
                'email': 'a@gmail.com',
                'username': "Emad"
            })

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

        # response should be 400 because emao; already exists
        response = self.client.post(
            path=self.viewset_url + 'activate/',
            data={
                'email': 'emad@gmail.com',
                'username': "A"
            })

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

        # response should be 200
        response = self.client.post(
            path=self.viewset_url + 'activate/',
            data={
                'email': 'new-email@gmail.com',
                'username': "new-username"
            })

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_set_password(self):

        # response should be 400 because email doesn't exist
        response = self.client.post(
            path=self.viewset_url + 'set-password/',
            data={
                'email': 'new-email@gmail.com',
                'username': "admin",
                'password': "emad1234",
                're_password': 'emad1234',
                'token': '4321'
            })

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

        # response should be 400 because password and re_password are not same
        response = self.client.post(
            path=self.viewset_url + 'set-password/',
            data={
                'email': 'admin@gmail.com',
                'username': "admin",
                'password': "emad1234",
                're_password': 'emad12345678',
                'token': '4321'
            })

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

        # response should be 400 because token is incorrect
        response = self.client.post(
            path=self.viewset_url + 'set-password/',
            data={
                'email': 'admin@gmail.com',
                'username': "admin",
                'password': "emad1234",
                're_password': 'emad1234',
                'token': '43217891'
            })

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

        # response should be 400 because username doesn't exist
        response = self.client.post(
            path=self.viewset_url + 'set-password/',
            data={
                'email': 'admin@gmail.com',
                'username': "new-username",
                'password': "emad1234",
                're_password': 'emad1234',
                'token': '4321'
            })

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # response should be 200
        response = self.client.post(
            path=self.viewset_url + 'set-password/',
            data={
                'email': 'admin@gmail.com',
                'username': "admin",
                'password': "emad1234",
                're_password': 'emad1234',
                'token': '4321'
            })

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_check_code(self):
        pass

    # @mock.patch('django.core.mail.EmailMessage.send', return_value=1)
    # def test_activation_email(self, mocked_email_send):

    #     response = self.client.post(
    #         path=self.viewset_url + 'activation-email/',
    #         data={
    #             'email': 'emad@gmail.com',
    #             'username': "emad"
    #         })

    #     self.assertEquals(response.status_code, status.HTTP_200_OK)
