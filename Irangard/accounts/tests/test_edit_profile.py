from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
# from . import models


# Create your tests here.
class TestUserProfile(APITestCase):
    
    def setUp(self):
        self.user = models.User.objects.create(username='morteza', full_name='Morteza Shaharabi', email='Morteza.shsh@gmail.com', password='mo1234')
        self.user.save()
        
    # def test_getProfile(self):
        
    #     response = self.client.get(reverse('accounts:user-profile', args=(self.user.username,)))
    #     self.assertEqual(response.status_code, 200)
        
    # def test_putProfile(self):
        
    #     data = {
    #         'username': 'morteza',
    #         'password':'mo1234',
    #     }
        
    #     #doesn't work :(
        
    #     # self.token = models.Token.objects.get(user__username="morteza")
    #     # self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token.key)
    #     # response = self.client.put(reverse('accounts:user-profile'), data)
    #     # self.assertEqual(response.status_code, 200)
    #     url = reverse('accounts:accounts-jwt-create')
    #     response = self.client.post(path='http://127.0.0.1:8000/accounts/auth/jwt/create',data={'username': 'morteza', 'password':'mo1234'})
    #     # resp = self.client.post('http://127.0.0.1:8000/accounts/auth/jwt/create', {'username': 'morteza', 'password':'mo1234'}, format='json')
    #     self.assertEqual(response.status_code, 200)
    #     # self.assertTrue('access' in resp.data)
    #     # token = resp.data['token']
    #     # print(token)
    #     # self.assertTrue('access' in resp.data)
    #     # token = resp.data['token']