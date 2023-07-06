from email.mime import image
from django.test import TestCase

from utils.constants import ActionDimondExchange
from ..models import Experience, Comment
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
        self.image_file = self.temporary_image("test.jpg")
        self.user = self.make_user("morteza", "mo1234", "morteza@gmail.com")
        self.user_two = self.make_user("ali", "mo1234", "ali@gmail.com")
        self.place = self.make_place("1", "اقامتگاه تستی", "این یک اقامتگاه تستی است.", True, self.user)
        self.experience = Experience.objects.create(title="test_xp", image=self.image_file, summary="test_summary", body="test_body", place=self.place, user=self.user)
        self.comment = Comment.objects.create(experience=self.experience, user=self.user, text='MEWO')
        self.reply = Comment.objects.create(experience=self.experience, user=self.user, parent=self.comment, text='reply')
    def post_experience(self, data, user):
        
        token = self.login(self.user.username, 'mo1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        
        response = self.client.post(self.url, data=data)
        return response.data
    
    def test_get_experiences(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_correct_retrieve_experience(self):
        retrieve_url = self.url + str(self.experience.id) + '/'
        response = self.client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_correct_retrieve_experience_non_anonymous_person_owner(self):
        token = self.login(self.user.username, 'mo1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        retrieve_url = self.url + str(self.experience.id) + '/'
        response = self.client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_correct_retrieve_experience_non_anonymous_person_not_owner(self):
        token = self.login(self.user_two.username, 'mo1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        retrieve_url = self.url + str(self.experience.id) + '/'
        response = self.client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_incorrect_retrieve_experience(self):
        retrieve_url = self.url + str(2000) + '/'
        response = self.client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_correct_post_experience(self):
        
        token = self.login(self.user.username, 'mo1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        image = self.temporary_image("test.jpg")
        user_dimonds_before_adding_exp = self.user.dimonds
        data = {
            "title": "new experience",
            "image": image,
            "summary": "new experience summary",
            "date_created": "",
            "place": self.place.id,
            "body": "new experience body",
        }

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.user.refresh_from_db()
        self.assertEqual(user_dimonds_before_adding_exp + ActionDimondExchange.WRITING_EXPERIENCE, 
                        self.user.dimonds
                    )
        
        
    def test_incorrect_post_experience_without_token(self):
        
        image = self.temporary_image("test.jpg")
        
        data = {
            "title": "new experience",
            "image": image,
            "summary": "new experience summary",
            "date_created": "",
            "place": self.place.id,
            "body": "new experience body",
        }

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        
    def test_incorrect_post_experience_incorrect_token(self):
        
        token = self.login(self.user.username, 'mo1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token + 'aa')
        image = self.temporary_image("test.jpg")
        
        data = {
            "title": "new experience",
            "image": image,
            "summary": "new experience summary",
            "date_created": "",
            "place": self.place.id,
            "body": "new experience body",
        }

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        
    # def test_incorrect_post_experience_incorrect_image(self):
        
    #     token = self.login(self.user.username, 'mo1234')
    #     self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
    #     image = self.temporary_image("test.jpg")
        
    #     data = {
    #         "title": "new experience",
    #         "image": "1234",
    #         "summary": "new experience summary",
    #         "date_created": "",
    #         "place": self.place.id,
    #         "body": "new experience body",
    #     }

    #     response = self.client.post(self.url, data=data)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        
    def test_incorrect_post_experience_incorrect_place(self):
        
        token = self.login(self.user.username, 'mo1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        image = self.temporary_image("test.jpg")
        
        data = {
            "title": "new experience",
            "image": image,
            "summary": "new experience summary",
            "date_created": "",
            "place": 200,
            "body": "new experience body",
        }

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        
    def test_incorrect_post_experience_without_place(self):
        
        token = self.login(self.user.username, 'mo1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        image = self.temporary_image("test.jpg")
        
        data = {
            "title": "new experience",
            "image": image,
            "summary": "new experience summary",
            "date_created": "",
            "body": "new experience body",
        }

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        
    def test_incorrect_post_experience_without_title(self):
        
        token = self.login(self.user.username, 'mo1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        image = self.temporary_image("test.jpg")
        
        data = {
            "image": image,
            "summary": "new experience summary",
            "date_created": "",
            "place": self.place.id,
            "body": "new experience body",
        }

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        
    def test_correct_post_experience_without_image(self):
        
        token = self.login(self.user.username, 'mo1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        image = self.temporary_image("test.jpg")
        
        data = {
            "title": "new experience",
            "summary": "new experience summary",
            "date_created": "",
            "place": self.place.id,
            "body": "new experience body",
        }

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        
    def test_correct_post_experience_without_summary(self):
        
        token = self.login(self.user.username, 'mo1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        image = self.temporary_image("test.jpg")
        
        data = {
            "title": "new experience",
            "image": image,
            "date_created": "",
            "place": self.place.id,
            "body": "new experience body",
        }

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        
    def test_correct_post_experience_without_date_created(self):
        
        token = self.login(self.user.username, 'mo1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        image = self.temporary_image("test.jpg")
        
        data = {
            "title": "new experience",
            "image": image,
            "summary": "new experience summary",
            "place": self.place.id,
            "body": "new experience body",
        }

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        
    def test_correct_post_experience_without_body(self):
        
        token = self.login(self.user.username, 'mo1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        image = self.temporary_image("test.jpg")
        
        data = {
            "title": "new experience",
            "image": image,
            "summary": "new experience summary",
            "date_created": "",
            "place": self.place.id,
        }

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        
    def test_correct_put_experience(self):
        
        token = self.login(self.user.username, 'mo1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        image = self.temporary_image("test.jpg")
        
        data = {
            "title": "updated experience",
            "image": image,
            "summary": "new updated summary",
            "date_created": "",
            "place": self.place.id,
            "body": "new updated body",
        }

        put_url = self.url + str(self.experience.id) + '/'
        response = self.client.put(put_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    def test_incorrect_put_experience_without_token(self):
        
        image = self.temporary_image("test.jpg")
        
        data = {
            "title": "updated experience",
            "image": image,
            "summary": "new updated summary",
            "date_created": "",
            "place": self.place.id,
            "body": "new updated body",
        }

        put_url = self.url + str(self.experience.id) + '/'
        response = self.client.put(put_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        
    def test_incorrect_put_experience_incorrect_token(self):
        
        token = self.login(self.user.username, 'mo1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token + 'aa')
        image = self.temporary_image("test.jpg")
        
        data = {
            "title": "updated experience",
            "image": image,
            "summary": "new updated summary",
            "date_created": "",
            "place": self.place.id,
            "body": "new updated body",
        }

        put_url = self.url + str(self.experience.id) + '/'
        response = self.client.put(put_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        
    def test_incorrect_put_experience_invalid_token(self):
        
        new_user = self.make_user("morteza-new", "mo1234-new", "morteza-new@gmail.com")
        
        token = self.login("morteza-new", "mo1234-new")
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        image = self.temporary_image("test.jpg")
        
        data = {
            "title": "updated experience",
            "image": image,
            "summary": "new updated summary",
            "date_created": "",
            "place": self.place.id,
            "body": "new updated body",
        }

        put_url = self.url + str(self.experience.id) + '/'
        response = self.client.put(put_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        
    # def test_incorrect_put_experience_incorrect_image(self):
        
    #     token = self.login(self.user.username, 'mo1234')
    #     self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
    #     image = self.temporary_image("test.jpg")
        
    #     data = {
    #         "title": "new experience",
    #         "image": "1234",
    #         "summary": "new experience summary",
    #         "date_created": "",
    #         "place": self.place.id,
    #         "body": "new experience body",
    #     }

    #     put_url = self.url + str(self.experience.id) + '/'
    #     response = self.client.put(put_url, data=data)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        
    def test_incorrect_put_experience_incorrect_place(self):
        
        token = self.login(self.user.username, 'mo1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        image = self.temporary_image("test.jpg")
        
        data = {
            "title": "new experience",
            "image": image,
            "summary": "new experience summary",
            "date_created": "",
            "place": 200,
            "body": "new experience body",
        }

        put_url = self.url + str(self.experience.id) + '/'
        response = self.client.put(put_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        
    def test_incorrect_put_experience_without_place(self):
        
        token = self.login(self.user.username, 'mo1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        image = self.temporary_image("test.jpg")
        
        data = {
            "title": "new experience",
            "image": image,
            "summary": "new experience summary",
            "date_created": "",
            "body": "new experience body",
        }

        put_url = self.url + str(self.experience.id) + '/'
        response = self.client.put(put_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        
    def test_incorrect_put_experience_without_title(self):
        
        token = self.login(self.user.username, 'mo1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        image = self.temporary_image("test.jpg")
        
        data = {
            "image": image,
            "summary": "new experience summary",
            "date_created": "",
            "place": self.place.id,
            "body": "new experience body",
        }

        put_url = self.url + str(self.experience.id) + '/'
        response = self.client.put(put_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        
    def test_correct_put_experience_without_image(self):
        
        token = self.login(self.user.username, 'mo1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        image = self.temporary_image("test.jpg")
        
        data = {
            "title": "new experience",
            "summary": "new experience summary",
            "date_created": "",
            "place": self.place.id,
            "body": "new experience body",
        }

        put_url = self.url + str(self.experience.id) + '/'
        response = self.client.put(put_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    def test_correct_put_experience_without_summary(self):
        
        token = self.login(self.user.username, 'mo1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        image = self.temporary_image("test.jpg")
        
        data = {
            "title": "new experience",
            "image": image,
            "date_created": "",
            "place": self.place.id,
            "body": "new experience body",
        }

        put_url = self.url + str(self.experience.id) + '/'
        response = self.client.put(put_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    def test_correct_put_experience_without_date_created(self):
        
        token = self.login(self.user.username, 'mo1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        image = self.temporary_image("test.jpg")
        
        data = {
            "title": "new experience",
            "image": image,
            "summary": "new experience summary",
            "place": self.place.id,
            "body": "new experience body",
        }

        put_url = self.url + str(self.experience.id) + '/'
        response = self.client.put(put_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    def test_correct_put_experience_without_body(self):
        
        token = self.login(self.user.username, 'mo1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        image = self.temporary_image("test.jpg")
        
        data = {
            "title": "new experience",
            "image": image,
            "summary": "new experience summary",
            "date_created": "",
            "place": self.place.id,
        }

        put_url = self.url + str(self.experience.id) + '/'
        response = self.client.put(put_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    def test_correct_delete_experience(self):
        
        token = self.login(self.user.username, 'mo1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        delete_url = self.url + str(self.experience.id) + '/'
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    
    def test_incorrect_delete_experience_without_token(self):
        
        delete_url = self.url + str(self.experience.id) + '/'
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        
    def test_incorrect_delete_experience_incorret_token(self):
        
        token = self.login(self.user.username, 'mo1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token + 'abc')
        delete_url = self.url + str(self.experience.id) + '/'
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        
    def test_incorrect_delete_experience_invalid_token(self):
        
        new_user = self.make_user("morteza-new", "mo1234-new", "morteza-new@gmail.com")
        
        token = self.login("morteza-new", "mo1234-new")
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        delete_url = self.url + str(self.experience.id) + '/'
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_feed_correct(self):
        token = self.login(self.user.username, 'mo1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        retrieve_url = self.url + 'feed/'
        response = self.client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_feed_incorrect_not_logged_in(self):
        retrieve_url = self.url + 'feed/'
        response = self.client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_comment_correct(self):
        token = self.login(self.user_two.username, 'mo1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            'text': 'HI'
        }
        res = self.client.post(f"{self.url}{self.experience.id}/comments/", data)
        print(res.json())
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_comment_incorrect_bad_args(self):
        token = self.login(self.user_two.username, 'mo1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            'textddd': 'HI'
        }
        res = self.client.post(f"{self.url}{self.experience.id}/comments/", data)
        print(res.json())
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_destroy_comment_correct(self):
        token = self.login(self.user.username, 'mo1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        res = self.client.delete(f"{self.url}{self.experience.id}/comments/{self.comment.id}/")
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_comment_correct(self):
        token = self.login(self.user.username, 'mo1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            'text': 'ARSHAM IS KING'
        }
        res = self.client.put(f"{self.url}{self.experience.id}/comments/{self.comment.id}/", data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_comment_create_reply_correct(self):
        token = self.login(self.user.username, 'mo1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            'text': 'ARSHAM IS KING'
        }
        res = self.client.post(f"{self.url}{self.experience.id}/comments/{self.comment.id}/reply/", data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_comment_reply_update_correct(self):
        token = self.login(self.user.username, 'mo1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            'text': 'ARSHAM IS KING'
        }
        res = self.client.put(f"{self.url}{self.experience.id}/comments/{self.comment.id}/reply/{self.reply.id}/", data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_comment_reply_update_correct(self):
        token = self.login(self.user.username, 'mo1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        res = self.client.delete(f"{self.url}{self.experience.id}/comments/{self.comment.id}/reply/{self.reply.id}/")
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_exp_by_place(self):
        token = self.login(self.user.username, 'mo1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        res = self.client.get(f"{self.url}place/{self.place.id}")
        self.assertEqual(res.status_code, status.HTTP_200_OK)