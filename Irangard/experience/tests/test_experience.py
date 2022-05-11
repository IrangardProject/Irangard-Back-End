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

class ExperienceTestCase(TestCase):
    
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
        image_file = self.temporary_image("test.jpg")
        self.user = self.make_user("morteza", "mo1234", "morteza@gmail.com")
        self.place = self.make_place("1", "اقامتگاه تستی", "این یک اقامتگاه تستی است.", True, self.user)
        # token = self.login(user.username, user.password)
        # self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        self.experience = Experience.objects.create(title="test_xp", image=image_file, summary="test_summary", body="test_body", place=self.place, user=self.user)
        
    
    def test_get_experiences(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_correct_retrieve_experience(self):
        retrieve_url = self.url + str(self.experience.id) + '/'
        response = self.client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_incorrect_retrieve_experience(self):
        retrieve_url = self.url + str(20) + '/'
        response = self.client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    