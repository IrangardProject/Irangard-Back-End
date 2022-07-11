from email.mime import image
from django.test import TestCase
from ..models import Experience
from places.models import Place
from accounts.models import User
from rest_framework.test import APIClient
import io
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
import json
from rest_framework import status

class LikeTestCase(TestCase):
    
    def temporary_image(self, name):
        bts = io.BytesIO()
        img = Image.new("RGB", (100, 100))
        img.save(bts, 'jpeg')
        return SimpleUploadedFile(name, bts.getvalue())
       
    def make_user(self, username, password, email):
        self.user = User.objects.create(username=username, email=email)
        self.user.set_password(password)
        self.user.save()
        return self.user
    
    def make_place(self, place_type, title, description, is_free, user):
        self.place = Place.objects.create(place_type=place_type, title=title, description=description, is_free=is_free, added_by=user)
        return self.place
    
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
        self.url = 'http://127.0.0.1:8000/experiences/'
        self.image_file = self.temporary_image("test.jpg")
        self.user = self.make_user("morteza", "mo1234", "morteza@gmail.com")
        self.place = self.make_place("1", "اقامتگاه تستی", "این یک اقامتگاه تستی است.", True, self.user)
        self.experience = Experience.objects.create(title="test_xp", image=self.image_file, summary="test_summary", body="test_body", place=self.place, user=self.user)
        
        
    def test_correct_like(self):
        
        token = self.login(self.user.username, 'mo1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        like_url = self.url + str(self.experience.id) + '/like'
        before_like_like_number = self.experience.like_number
        
        response = self.client.post(like_url)
        new_experience_id = response.data['experience']
        new_experience = Experience.objects.get(pk=new_experience_id)
        after_like_like_number = new_experience.like_number
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(int(after_like_like_number), int(before_like_like_number) + 1)
        
        
    def test_incorrect_like_without_token(self):

        like_url = self.url + str(self.experience.id) + '/like'
        before_like_like_number = self.experience.like_number
        
        response = self.client.post(like_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        
    def test_incorrect_like_incorrect_token(self):
        
        token = self.login(self.user.username, 'mo1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token + 'aabbcc')

        like_url = self.url + str(self.experience.id) + '/like'
        before_like_like_number = self.experience.like_number
        
        response = self.client.post(like_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        
    def test_incorrect_like_liked_before(self):
        
        token = self.login(self.user.username, 'mo1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        like_url = self.url + str(self.experience.id) + '/like'
        before_like_like_number = self.experience.like_number
        
        response = self.client.post(like_url)
        
        new_response = self.client.post(like_url)
        self.assertEqual(new_response.status_code, status.HTTP_400_BAD_REQUEST)
        
        
    def test_correct_unlike(self):
        token = self.login(self.user.username, 'mo1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        like_url = self.url + str(self.experience.id) + '/like'
        before_like_like_number = self.experience.like_number
        
        response = self.client.post(like_url)
        new_experience_id = response.data['experience']
        new_experience = Experience.objects.get(pk=new_experience_id)
        after_like_like_number = new_experience.like_number
        
        unlike_url = self.url + str(self.experience.id) + '/unlike'
        new_response = self.client.post(unlike_url)
        # print(new_response.data)
        unlike_experience_id = response.data['experience']
        new_unlike_experience = Experience.objects.get(pk=unlike_experience_id)
        after_unlike_like_number = new_unlike_experience.like_number
        
        self.assertEqual(new_response.status_code, status.HTTP_200_OK)
        self.assertEqual(int(after_unlike_like_number), int(before_like_like_number))
        
    def test_correct_unlike_2(self):
        token = self.login(self.user.username, 'mo1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        like_url = self.url + str(self.experience.id) + '/like'
        before_like_like_number = self.experience.like_number
        
        response = self.client.post(like_url)
        new_experience_id = response.data['experience']
        new_experience = Experience.objects.get(pk=new_experience_id)
        after_like_like_number = new_experience.like_number
        
        unlike_url = self.url + str(self.experience.id) + '/unlike'
        new_response = self.client.post(unlike_url)
        unlike_experience_id = response.data['experience']
        new_unlike_experience = Experience.objects.get(pk=unlike_experience_id)
        after_unlike_like_number = new_unlike_experience.like_number
        
        self.assertEqual(new_response.status_code, status.HTTP_200_OK)
        self.assertEqual(int(after_unlike_like_number), int(after_like_like_number) - 1)
        
        
    def test_incorrect_unlike_without_token(self):

        like_url = self.url + str(self.experience.id) + '/like'
        before_like_like_number = self.experience.like_number
        
        response = self.client.post(like_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        
    def test_incorrect_unlike_incorrect_token(self):
        
        token = self.login(self.user.username, 'mo1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token + 'aabbcc')

        like_url = self.url + str(self.experience.id) + '/like'
        before_like_like_number = self.experience.like_number
        
        response = self.client.post(like_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    
    def test_incorrect_like_hasnot_liked_before(self):
        
        token = self.login(self.user.username, 'mo1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        unlike_url = self.url + str(self.experience.id) + '/unlike'
        
        response = self.client.post(unlike_url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)   
        
        
    def test_incorrect_unlike_unliked_before(self):
        token = self.login(self.user.username, 'mo1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        like_url = self.url + str(self.experience.id) + '/like'
        before_like_like_number = self.experience.like_number
        
        response = self.client.post(like_url)
        new_experience_id = response.data['experience']
        new_experience = Experience.objects.get(pk=new_experience_id)
        after_like_like_number = new_experience.like_number
        
        unlike_url = self.url + str(self.experience.id) + '/unlike'
        new_response = self.client.post(unlike_url)
        new_unlike_response = self.client.post(unlike_url)
        
        self.assertEqual(new_unlike_response.status_code, status.HTTP_400_BAD_REQUEST)
        