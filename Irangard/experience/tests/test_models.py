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
    
    def temporary_image(self):
        bts = io.BytesIO()
        img = Image.new("RGB", (100, 100))
        img.save(bts, 'jpeg')
        return SimpleUploadedFile("test.jpg", bts.getvalue())
       
    def make_user(self):
        self.user = User.objects.create(username="morteza", email="morteza@gmail.com")
        self.user.set_password("mo1234")
        self.user.save()
        return self.user
    
    def make_place(self):
        self.place = Place.objects.create(place_type='1', title="اقامتگاه تستی", description="این یک اقامتگاه تستی است.", is_free=True, added_by=self.user)
        return self.place
    
    def login(self, username, password):
        # print(username, password)
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
        image_file = self.temporary_image()
        self.user = self.make_user()
        self.place = self.make_place()
        token = self.login(self.user.username, self.user.password)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        Experience.objects.create(title="test_xp", image=image_file, summary="test_summary", body="test_body", place=self.place, user=self.user)
        
    def test_title(self):
        experience = Experience.objects.get(title="test_xp")
        self.assertEqual(experience.title, "test_xp")
        
    def test_summary(self):
        experience = Experience.objects.get(summary="test_summary")
        self.assertEqual(experience.title, "test_xp")
        
    def test_body(self):
        experience = Experience.objects.get(body="test_body")
        self.assertEqual(experience.title, "test_xp")
        
    def test_place(self):
        experience = Experience.objects.get(place=self.place)
        self.assertEqual(experience.title, "test_xp")
        
    def test_user(self):
        experience = Experience.objects.get(user=self.user)
        self.assertEqual(experience.title, "test_xp")