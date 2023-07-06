from django.test import TestCase
from django.urls import reverse
from accounts.models import User
from rest_framework.test import APIClient
import json
from rest_framework import status
import io
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile


# Create your tests here.
class TestUserProfile(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username="morteza", email="morteza@gmail.com")
        self.user.set_password("mo1234")
        self.user.save()
        self.user1 = User.objects.create(username="amir", email="amir@gmail.com")
        self.user1.set_password("123456")
        self.user1.save()
        self.admin_user = User.objects.create(username="admin", email="admin@gmail.com")
        self.admin_user.set_password("admin")
        self.admin_user.is_admin = True
        self.admin_user.save()
        self.url = 'http://127.0.0.1:8000/accounts/'
        
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
        
    def temporary_image(self):
        bts = io.BytesIO()
        img = Image.new("RGB", (100, 100))
        img.save(bts, 'jpeg')
        return SimpleUploadedFile("test.jpg", bts.getvalue())
        
    def test_incorrect_login_incorrect_email(self):
        
        #uncorrect username
        url = reverse('accounts:accounts-jwt-create')
        response = self.client.post(url, {"username":"morteza2","password":"mo1234"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_incorrect_login_incorrect_email(self):
        #uncorrect email
        url = reverse('accounts:accounts-jwt-create')
        response = self.client.post(url, {"username":"morteza2@gmail.com","password":"mo1234"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_incorrect_login_incorrect_password(self):
        #uncorrect password
        url = reverse('accounts:accounts-jwt-create')
        response = self.client.post(url, {"username":"morteza","password":"mo12342"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_incorrect_login_no_password(self):
        #no password
        url = reverse('accounts:accounts-jwt-create')
        response = self.client.post(url, {"username":"morteza"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_incorrect_login_no_usernname(self):
        #no username
        url = reverse('accounts:accounts-jwt-create')
        response = self.client.post(url, {"password":"mo12342"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_correct_login_with_username(self):
        #correct login with username
        url = reverse('accounts:accounts-jwt-create')
        response = self.client.post(url, {"username":"morteza","password":"mo1234"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('refresh' in response.data)
        self.assertTrue('access' in response.data)
        
    def test_correct_login_with_email(self):
        #correct login with email
        url = reverse('accounts:accounts-jwt-create')
        response = self.client.post(url, {"username":"morteza@gmail.com","password":"mo1234"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('refresh' in response.data)
        self.assertTrue('access' in response.data)
        
    def test_getProfile_fail(self):
        
        #fail response
        self.uncorrect_username = "Hello"
        response = self.client.get(reverse('accounts:user-profile', args=(self.uncorrect_username,)))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_getProfile_success(self):
        #ok response
        response = self.client.get(reverse('accounts:user-profile', args=(self.user.username,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_correct_putProfile(self):
        
        #correct login with username
        access_token = self.login("morteza", "mo1234")
        image_file = self.temporary_image()
        
        put_data = {
            "username":"morteza", 
            "image": image_file,
            "about_me":"I'm Morteza Shahrabi Farahani. Backend developer at Irangard.",
            "is_special": True,
            "full_name": "Morteza Shahrabi Farahani",
        }
        
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + access_token)
        
        url = reverse('accounts:user-profile', args=(self.user.username,))
        response = self.client.put(url, data=put_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_incorrect_putProfile_incorrect_token(self):
        
        #correct login with username but incorrect token
        access_token = self.login("morteza", "mo1234")
        new_access_token = access_token + "a"
        image_file = self.temporary_image()
    
        put_data = {
            "username":"morteza", 
            "image": image_file,
            "about_me":"I'm Morteza Shahrabi Farahani. Backend developer at Irangard.",
            "is_special": True,
            "full_name": "Morteza Shahrabi Farahani",
            
        }
        
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + new_access_token)
        
        url = reverse('accounts:user-profile', args=(self.user.username,))
        response = self.client.put(url, data=put_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_incorrect_putProfile_without_token(self):
    
        put_data = {
            "username":"morteza", 
            "about_me":"I'm Morteza Shahrabi Farahani. Backend developer at Irangard.",
            "is_special": True,
            "full_name": "Morteza Shahrabi Farahani",
            
        }
        
        self.client.credentials(HTTP_AUTHORIZATION='JWT ')
        
        url = reverse('accounts:user-profile', args=(self.user.username,))
        response = self.client.put(url, data=put_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_incorrect_putProfile_without_token_2(self):
    
        put_data = {
            "username":"morteza", 
            "about_me":"I'm Morteza Shahrabi Farahani. Backend developer at Irangard.",
            "is_special": True,
            "full_name": "Morteza Shahrabi Farahani",
            
        }
        
        url = reverse('accounts:user-profile', args=(self.user.username,))
        response = self.client.put(url, data=put_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_correct_putProfile_change_username(self):
        
        #correct login with username
        access_token = self.login("morteza", "mo1234")
        image_file = self.temporary_image()
        
        put_data = {
            "username":"morteza1", 
            "image": image_file,
            "about_me":"I'm Morteza Shahrabi Farahani. Backend developer at Irangard.",
            "is_special": True,
            "full_name": "Morteza Shahrabi Farahani",
        }
        
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + access_token)
        
        url = reverse('accounts:user-profile', args=(self.user.username,))
        response = self.client.put(url, data=put_data)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], "morteza1")
        
    def test_correct_putProfile_change_about_me(self):
        
        #correct login with username
        access_token = self.login("morteza", "mo1234")
        image_file = self.temporary_image()
        
        put_data = {
            "username":"morteza", 
            "image": image_file,
            "about_me":"I'm Morteza Shahrabi Farahani. Backend developer at Irangard. Computer enginering student at IUST",
            "is_special": True,
            "full_name": "Morteza Shahrabi Farahani",
        }
        
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + access_token)
        
        url = reverse('accounts:user-profile', args=(self.user.username,))
        response = self.client.put(url, data=put_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['about_me'], "I'm Morteza Shahrabi Farahani. Backend developer at Irangard. Computer enginering student at IUST")
        
    def test_correct_putProfile_change_is_special(self):
        
        #correct login with username
        access_token = self.login("morteza", "mo1234")
        image_file = self.temporary_image()
        
        put_data = {
            "username":"morteza1", 
            "image": image_file,
            "about_me":"I'm Morteza Shahrabi Farahani. Backend developer at Irangard.",
            "is_special": False,
            "full_name": "Morteza Shahrabi Farahani",
        }
        
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + access_token)
        
        url = reverse('accounts:user-profile', args=(self.user.username,))
        response = self.client.put(url, data=put_data)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_special'], False)
        
    def test_correct_putProfile_change_full_name(self):
        
        #correct login with username
        access_token = self.login("morteza", "mo1234")
        image_file = self.temporary_image()
        
        put_data = {
            "username":"morteza1", 
            "image": image_file,
            "about_me":"I'm Morteza Shahrabi Farahani. Backend developer at Irangard.",
            "is_special": False,
            "full_name": "Morteza Shahrabi Farahani test",
        }
        
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + access_token)
        
        url = reverse('accounts:user-profile', args=(self.user.username,))
        response = self.client.put(url, data=put_data)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['full_name'], "Morteza Shahrabi Farahani test")
        
        
    def test_correct_putProfile_change_image(self):
        
        #correct login with username
        access_token = self.login("morteza", "mo1234")
        image_file = self.temporary_image()
        # print("image type is: ",type(image_file))
        
        put_data = {
            "username":"morteza1", 
            "image": image_file,
            "about_me":"I'm Morteza Shahrabi Farahani. Backend developer at Irangard.",
            "is_special": False,
            "full_name": "Morteza Shahrabi Farahani test",
        }
        
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + access_token)
        
        url = reverse('accounts:user-profile', args=(self.user.username,))
        response = self.client.put(url, data=put_data)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data['image'].startswith("https://res.cloudinary.com/dgwbbbisy/image/upload/v1/media/images"), True)
        
    def test_correct_putProfile_all(self):
        
        #correct login with username
        access_token = self.login("morteza", "mo1234")
        image_file = self.temporary_image()
        
        put_data = {
            "username":"morteza1", 
            "image": image_file,
            "about_me":"I'm Morteza Shahrabi Farahani. Backend developer at Irangard. 1",
            "is_special": False,
            "full_name": "Morteza Shahrabi Farahani test",
        }
        
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + access_token)
        
        url = reverse('accounts:user-profile', args=(self.user.username,))
        response = self.client.put(url, data=put_data)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['full_name'], "Morteza Shahrabi Farahani test")
        self.assertEqual(response.data['is_special'], False)
        self.assertEqual(response.data['about_me'], "I'm Morteza Shahrabi Farahani. Backend developer at Irangard. 1")
        self.assertEqual(response.data['username'], "morteza1")
        # self.assertEqual(response.data['image'].startswith("https://res.cloudinary.com/dgwbbbisy/image/upload/v1/media/images"), True)
        
        
    def test_incorrect_putProfile_incorrect_data(self):
        
        #correct login with username
        access_token = self.login("morteza", "mo1234")
        
        put_data = {
            "about_me":"I'm Morteza Shahrabi Farahani. Backend developer at Irangard.",
            "is_special": False,
            "full_name": "Morteza Shahrabi Farahani test",
        }
        
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + access_token)
        
        url = reverse('accounts:user-profile', args=(self.user.username,))
        response = self.client.put(url, data=put_data, format='json')
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 
        
        
    def test_correct_putProfile_without_about_me(self):
        
        #correct login with username
        access_token = self.login("morteza", "mo1234")
        
        put_data = {
            "username":"morteza", 
            "is_special": True,
            "full_name": "Morteza Shahrabi Farahani",
            
        }
        
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + access_token)
        
        url = reverse('accounts:user-profile', args=(self.user.username,))
        response = self.client.put(url, data=put_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_correct_putProfile_without_is_special(self):
        
        #correct login with username
        access_token = self.login("morteza", "mo1234")
        
        put_data = {
            "username":"morteza", 
            "full_name": "Morteza Shahrabi Farahani",
        }
        
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + access_token)
        
        url = reverse('accounts:user-profile', args=(self.user.username,))
        response = self.client.put(url, data=put_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_correct_putProfile_without_full_name(self):
        
        #correct login with username
        access_token = self.login("morteza", "mo1234")
        
        put_data = {
            "username":"morteza", 
        }
        
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + access_token)
        
        url = reverse('accounts:user-profile', args=(self.user.username,))
        response = self.client.put(url, data=put_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_correct_putProfile_without_image(self):
        
        #correct login with username
        access_token = self.login("morteza", "mo1234")
        
        put_data = {
            "username":"morteza", 
        }
        
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + access_token)
        
        url = reverse('accounts:user-profile', args=(self.user.username,))
        response = self.client.put(url, data=put_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
      
    def test_incorrect_putProfile_bad_username(self):
        
        #correct login with username
        access_token = self.login("morteza", "mo1234")
        
        put_data = {
            "username123": "morteza", 
            "about_me":"I'm Morteza Shahrabi Farahani. Backend developer at Irangard.",
            "is_special": True,
            "full_name": "Morteza Shahrabi Farahani",
            
        }
        
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + access_token)
        
        url = reverse('accounts:user-profile', args=(self.user.username,))
        response = self.client.put(url, data=put_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    
    def test_get_followers(self):
        url = self.url + str(self.user.pk) + '/followers/'
        token = self.login("admin", "admin")
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    
    def test_get_following(self):
        url = self.url + str(self.user.pk) + '/following/'
        token = self.login("admin", "admin")
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
    def test_correct_follow(self):
        url = self.url + str(self.user.pk) + '/follow/'
        token = self.login(self.user1.username, "123456")
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
    def test_incorrect_follow_followed_before(self):
        self.user1.following.add(self.user)
        self.user1.save()
        url = self.url + str(self.user.pk) + '/follow/'
        token = self.login(self.user1.username, "123456")
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
        
    def test_correct_follow(self):
        self.user1.following.add(self.user)
        self.user1.save()
        url = self.url + str(self.user.pk) + '/unfollow/'
        token = self.login(self.user1.username, "123456")
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
    def test_incorrect_unfollow_not_followed_before(self):
        url = self.url + str(self.user.pk) + '/unfollow/'
        token = self.login(self.user1.username, "123456")
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    
    def test_update_favorite_types(self):
        url = self.url + str(self.user.pk) + '/update_favorite_types/'
        token = self.login(self.user.username, "mo1234")
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {
            "favorite_events" : [1, 2],
            "favorite_tours" : [1, 2]
        }
        response = self.client.post(url, format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
    def test_correct_get_user_information(self):
        url = self.url + 'information'
        token = self.login(self.user.username, "mo1234")
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_incorrect_get_user_information(self):
        url = self.url + 'information'
        token = self.login(self.user.username, "mo1234")
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token + "aa")
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    
    def test_correct_get_claim_place_ownership(self):
        url = self.url + 'claimed-places'
        token = self.login(self.user.username, "mo1234")
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    def test_correct_who_is(self):
        url = self.url + 'who-is'
        token = self.login(self.user.username, "mo1234")
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    def test_correct_get_all_users(self):
        url = self.url + 'users'
        token = self.login(self.user.username, "mo1234")
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        