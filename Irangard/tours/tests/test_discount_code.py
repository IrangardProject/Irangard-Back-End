from django.test import TestCase, Client
from rest_framework import status
from django.urls import reverse
from ..models import *
import json
from rest_framework.test import APIClient

class DiscountCodeTestcase(TestCase):

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
        self.url = 'http://127.0.0.1:8000/tours/'
        self.user = self.make_user("amir", "123456", "amir@gmail.com")
        self.cheater_user = self.make_user("cheater", "123456", "cheater@gmail.com")
        self.admin_user = self.make_admin_user("admin", "123456", "admin@gmail.com")
        # create main super-user
        self.special_user = SpecialUser.objects.create(
            user=self.user, total_revenue=0)
        self.special_user.save()
        # end create main super-user

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

        self.data = {
            "title": "first_test_tour",
            "cost": 200,
            "capacity": 50,
            "remaining": 50,
            "start_date": "2030-05-22T15:49:49.505Z",
            "end_date": "2030-05-28T15:49:49.505Z",
            "tour_type": "0",
            "province": "Tehran",
            "city": "Tehran"
        }
        self.data_1 = {
            "title": "test_tour",
            "cost": 400,
            "capacity": 50,
            "remaining": 50,
            "start_date": "2030-05-15T15:49:49.505Z",
            "end_date": "2030-05-23T15:49:49.505Z",
            "tour_type": "1",
            "province": "Tehran",
            "city": "Tehran"
        }

        discount_data = {
            'off_percentage' : 10,
            'expire_date' : '2024-05-19 10:10:19+00:00',
            'code': 'HELLOSUMMER',
        }
        self.tour = Tour.objects.create(**self.data, owner=self.special_user, status=StatusMode.ACCEPTED)
        self.tour1 = Tour.objects.create(**self.data_1, owner=self.second_special_user, status=StatusMode.ACCEPTED)
        self.tour2 = Tour.objects.create(**self.data_1, owner=self.special_user, status=StatusMode.ACCEPTED)
        self.discount1 = DiscountCode.objects.create(**discount_data, tour=self.tour2)
        self.discount2 = DiscountCode.objects.create(**discount_data, tour=self.tour1)
        self.pending_tour = Tour.objects.create(**self.data, owner=self.special_user)


    def test_create_discount_code_bad_404_tour(self):
        token = self.login(self.user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        res = self.client.post(f"{self.url}{40000}/discount-codes/")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_discount_code_ok(self):
        token = self.login(self.user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            'off_percentage' : 10,
            'expire_date' : '2024-05-19 10:10:19+00:00',
            'code': 'HELLOSUMMER',
        }
        res = self.client.post(f"{self.url}{self.tour.id}/discount-codes/", data)
        print(res.json())
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_discount_code_bad_args(self):
        token = self.login(self.user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            'off_percentage': 10,
            'expire_date': '2024-05-19',
            'code': 'HELLOSUMMER',
        }
        res = self.client.post(f"{self.url}{self.tour.id}/discount-codes/", data)
        print(res.json())
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_discount_code_bad_not_logged_in(self):
        data = {
            'off_percentage': 10,
            'expire_date': '2024-05-19',
            'code': 'HELLOSUMMER',
        }
        res = self.client.post(f"{self.url}{self.tour.id}/discount-codes/", data)
        print(res.json())
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_discount_code_list_ok(self):
        res = self.client.get(f"{self.url}{self.tour.id}/discount-codes/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_discount_code_retrieve_bad_404(self):
        token = self.login(self.user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        res = self.client.get(f"{self.url}{self.tour.id}/discount-codes/{5000}/")
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_discount_code_retrieve_bad_bad_url(self):
        token = self.login(self.user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        res = self.client.get(f"{self.url}{self.tour.id}/discount-codes/{5000}")
        self.assertEqual(res.status_code, status.HTTP_301_MOVED_PERMANENTLY)

    def test_discount_code_retrieve_bad_request_method(self):
        token = self.login(self.user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        res = self.client.post(f"{self.url}{self.tour.id}/discount-codes/{5000}/")
        self.assertEqual(res.status_code, status.HTTP_301_MOVED_PERMANENTLY)

    def test_discount_code_retrieve_bad_request_method(self):
        token = self.login(self.user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        res = self.client.post(f"{self.url}{self.tour.id}/discount-codes/{5000}/")
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_discount_code_retrieve_ok(self):
        token = self.login(self.user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        res = self.client.get(f"{self.url}{self.tour2.id}/discount-codes/{self.discount1.id}/")
        print(self.discount1.id)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_discount_code_destroy_ok(self):
        token = self.login(self.user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        res = self.client.delete(f"{self.url}{self.tour2.id}/discount-codes/{self.discount1.id}/")
        print(self.discount1.id)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_discount_code_destroy_bad_permission_denied(self):
        token = self.login(self.user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        res = self.client.delete(f"{self.url}{self.tour1.id}/discount-codes/{self.discount2.id}/")
        print(self.discount1.id)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_discount_code_update_ok(self):
        token = self.login(self.user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        discount_data = {
            'off_percentage': 20,
            'expire_date': '2024-05-19 10:10:19+00:00',
            'code': 'HELLOSUMMER',
        }
        res = self.client.put(f"{self.url}{self.tour2.id}/discount-codes/{self.discount1.id}/", discount_data)
        print(self.discount1.id)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_discount_code_update_bad_permission_denied(self):
        token = self.login(self.user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        discount_data = {
            'off_percentage': 20,
            'expire_date': '2024-05-19 10:10:19+00:00',
            'code': 'HELLOSUMMER',
        }
        res = self.client.delete(f"{self.url}{self.tour1.id}/discount-codes/{self.discount2.id}/", discount_data)
        print(self.discount1.id)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)