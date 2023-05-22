import json
from django.utils.dateparse import parse_date
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.http import HttpRequest
from rest_framework import permissions, status
from rest_framework.response import Response

from utils.constants import ActionDimondExchange
from ..models import *
from accounts.models import User, SpecialUser
from datetime import datetime


def parse_date(date_str):
    return datetime.strptime(date_str[:19], '%Y-%m-%dT%H:%M:%S')


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

    
    def make_admin_user(self, username, password, email):
        user = User.objects.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
    

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
        
        self.data_1 ={
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

        self.tour = Tour.objects.create(**self.data, owner=self.special_user, status=StatusMode.ACCEPTED)
        self.tour1 = Tour.objects.create(**self.data_1, owner=self.special_user, status=StatusMode.ACCEPTED)
        self.tour2 = Tour.objects.create(**self.data_1, owner=self.special_user, status=StatusMode.ACCEPTED)
        self.pending_tour = Tour.objects.create(**self.data, owner=self.special_user)
        
        self.admin_user = self.make_admin_user("admin", "123456", "admin@gmail.com")  
    
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

    
    def test_tour_create_ignore_status_field(self):
        data = self.data.copy()
        data["status"] = StatusMode.ACCEPTED
        data["title"] = "from test_tour_create_ignore_status_field"
        response = self.client.post(self.url, json.dumps(
            data, indent=4, sort_keys=True, default=str), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_tour = Tour.objects.get(title="from test_tour_create_ignore_status_field")
        self.assertEqual(new_tour.status, StatusMode.PENDING)
        
        
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
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    def test_pending_tour_update(self):
        data = self.data.copy()
        data['title'] = 'test_title'
        data['cost'] = 100
        response = self.client.put(self.url + f'{self.pending_tour.id}/', json.dumps(
            data, indent=4, sort_keys=True, default=str), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    
    def test_tour_update_ignore_status_field(self):
        data = self.data.copy()
        data['title'] = 'test_title'
        data['cost'] = 100
        data["status"] = StatusMode.DENIED
        response = self.client.put(self.url + f'{self.tour.id}/', json.dumps(
            data, indent=4, sort_keys=True, default=str), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.tour.refresh_from_db()
        self.assertEqual(self.tour.status, StatusMode.ACCEPTED)

        
    def test_tour_update_incorrect_url(self):
        data = self.data.copy()
        data['title'] = 'test_title'
        data['cost'] = 100
        response = self.client.put(self.url + "bug" + f'{self.tour.id}/', json.dumps(
            data, indent=4, sort_keys=True, default=str), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_tour_partial_update(self):
        data = {"title": "test_title"}
        response = self.client.patch(self.url + f'{self.tour.id}/', json.dumps(
            data, indent=4, sort_keys=True, default=str), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)


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
        token = self.login(self.user.username, 'emad1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.delete(f"{self.url}{self.tour.id}/")
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
            
    
    def test_tour_title_contains_filter(self):
        response = self.client.get(self.url + '?title__contains=fir')
        response_dict = json.loads(response.content)
        tour_list = response_dict['results']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for tour in tour_list:
            self.assertEqual("fir" in tour["title"], True)
        
        
    def test_tour_cost_lte_filter(self):
        response = self.client.get(self.url + '?cost__lte=300')
        response_dict = json.loads(response.content)
        tour_list = response_dict['results']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for tour in tour_list:
            self.assertLessEqual(int(tour["cost"]), 300)
            
    
    def test_tour_cost_gte_filter(self):
        response = self.client.get(self.url + '?cost__gte=300')
        response_dict = json.loads(response.content)
        tour_list = response_dict['results']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for tour in tour_list:
            self.assertGreaterEqual(int(tour["cost"]), 300)


    def test_tour_start_date_lte_filter(self):
        date_str = "2022-05-16T00:00:00.505Z"
        response = self.client.get(self.url + f'?start_date__lte={date_str}')
        response_dict = json.loads(response.content)
        tour_list = response_dict['results']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for tour in tour_list:
            self.assertLessEqual(
                parse_date(tour["start_date"]), parse_date(date_str))
            
            
    def test_tour_start_date_gte_filter(self):
        date_str = "2022-05-16T00:00:00.505Z"
        response = self.client.get(self.url + f'?start_date__gte={date_str}')
        response_dict = json.loads(response.content)
        tour_list = response_dict['results']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for tour in tour_list:
            self.assertGreaterEqual(
                parse_date(tour["start_date"]), parse_date(date_str))
            
    
    def test_tour_end_date_lte_filter(self):
        date_str = "2022-05-25T00:00:00.505Z"
        response = self.client.get(self.url + f'?end_date__lte={date_str}')
        response_dict = json.loads(response.content)
        tour_list = response_dict['results']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for tour in tour_list:
            self.assertLessEqual(
                parse_date(tour["end_date"]), parse_date(date_str))
            
            
    def test_tour_end_date_gte_filter(self):
        date_str = "2022-05-25T00:00:00.505Z"
        response = self.client.get(self.url + f'?end_date__gte={date_str}')
        response_dict = json.loads(response.content)
        tour_list = response_dict['results']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for tour in tour_list:
            self.assertGreaterEqual(
                parse_date(tour["end_date"]), parse_date(date_str))
    
    
    def test_tour_book(self):
        pass

    def test_tour_book_not_authenticated(self):
        pass

    def test_tour_verify(self):
        pass


    # tour email notification tests !
    def test_tour_email_notification(self):
        self.user.favorite_tour_types = ['0', '1', '2', '3']
        self.user.save()
        data_1 = {
            "title": "test_tour",
            "cost": 400,
            "capacity": 50,
            "remaining": 50,
            "start_date": "2022-05-15T15:49:49.505Z",
            "end_date": "2022-05-23T15:49:49.505Z",
            "tour_type": "1"
        }
        email_queue_count = EmailQueue.objects.count()
        tour = Tour.objects.create(**self.data, owner=self.special_user)
        tour.save()
        new_email_queue = EmailQueue.objects.count()
        self.assertEqual(new_email_queue - email_queue_count, 1)
        self.assertEqual(EmailQueue.objects.all().last().state, '0')
    
    
    def test_correct_accept_tour_admin_user(self):
        user_dimond_before_activate = self.pending_tour.owner.user.dimonds
        token = self.login(self.admin_user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.put(f"{self.url}{self.pending_tour.pk}/admin_acceptance/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.pending_tour.refresh_from_db()
        self.assertEqual(self.pending_tour.status, StatusMode.ACCEPTED)
        self.assertEqual(user_dimond_before_activate + ActionDimondExchange.ORGANIZING_TOUR, 
                        self.pending_tour.owner.user.dimonds
                    )
    
    
    def test_incorrect_accept_tour_without_token(self):
        client = APIClient()
        response = client.put(f"{self.url}{self.pending_tour.pk}/admin_acceptance/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    
    def test_incorrect_accept_tour_normal_user_token(self):
        token = self.login(self.user.username, 'emad1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.put(f"{self.url}{self.pending_tour.pk}/admin_acceptance/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    
    def test_correct_deny_tour_admin_user(self):
        token = self.login(self.admin_user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.put(f"{self.url}{self.pending_tour.pk}/admin_denial/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.pending_tour.refresh_from_db()
        self.assertTrue(self.pending_tour.status, StatusMode.ACCEPTED)
    
    
    def test_incorrect_deny_tour_without_token(self):
        client = APIClient()
        response = client.put(f"{self.url}{self.pending_tour.pk}/admin_denial/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    
    def test_incorrect_deny_tour_normal_user_token(self):
        token = self.login(self.user.username, 'emad1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.put(f"{self.url}{self.pending_tour.pk}/admin_denial/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    
    def test_correct_get_pending_tours_admin_user(self):
        token = self.login(self.admin_user.username, '123456')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(f"{self.url}pending_tours/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for tour in response.data:
            self.assertEqual(tour["status"], StatusMode.PENDING)

    
    def test_incorrect_get_pending_tours_without_token(self):
        client = APIClient()
        response = client.get(f"{self.url}pending_tours/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    
    def test_incorrect_get_pending_tours_normal_user(self):
        response = self.client.get(f"{self.url}pending_tours/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # def test_tour_pay_book_cost_from_wallet_success(self):
    #     self.user.wallet_credit = 200
    #     self.user.save()
    #     client = APIClient()
    #     response = client.post(f"{self.url}book_with_wallet/{self.tour.id}")
    #     print(response)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)