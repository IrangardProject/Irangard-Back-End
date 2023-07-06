from django.test import TestCase, Client
from rest_framework import status
from django.urls import reverse
from ..models import *
import json
from rest_framework.test import APIClient

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


    def setUp(self):
        self.client = APIClient()
        self.url = 'http://127.0.0.1:8000/accounts/'
        self.user = self.make_user("amir", "123456", "amir@gmail.com")
        self.cheater_user = self.make_user("cheater", "123456", "cheater@gmail.com")
        self.admin_user = self.make_admin_user("admin", "123456", "admin@gmail.com")

    def test_decrease_wallet_credit_wrong_args(self):
        token = self.login(self.user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        self.user.wallet_credit = 100
        self.user.save()
        data = {'wrong_input': 100}
        response = self.client.post(self.url +'wallet/decrease/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_decrease_wallet_credit_bad_not_logged_in(self):
        self.user.wallet_credit = 100
        self.user.save()
        data = {'amount': 100}
        response = self.client.post(self.url +'wallet/decrease/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_decrease_wallet_credit_bad_wrong_args(self):
        token = self.login(self.user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {'wrong_input': 100}
        response = self.client.post(self.url +'wallet/decrease/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_decrease_wallet_credit_bad_not_enough_credit(self):
        token = self.login(self.user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        self.user.wallet_credit = 100
        self.user.save()
        data = {'amount': 110}
        response = self.client.post(self.url +'wallet/decrease/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_decrease_wallet_credit_ok(self):
        token = self.login(self.user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        self.user.wallet_credit = 100
        self.user.save()
        data = {'amount': 100}
        response = self.client.post(self.url +'wallet/decrease/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['credit'], 0)

    def test_upgrade_to_super_user_bad_not_logged_in(self):
        response = self.client.post(self.url + 'wallet/user/upgrade/', format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_upgrade_to_super_user_bad_already_super_user(self):
        user = self.admin_user
        token = self.login(user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.post(self.url + 'wallet/user/upgrade/', format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_upgrade_to_super_user_bad_not_enough_credit(self):
        self.user.wallet_credit = 10000 - 100
        self.user.save()
        token = self.login(self.user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.post(self.url + 'wallet/user/upgrade/', format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_upgrade_to_super_user_ok(self):
        token = self.login(self.user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        self.user.wallet_credit = 10000
        self.user.save()
        response = self.client.post(self.url + 'wallet/user/upgrade/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)