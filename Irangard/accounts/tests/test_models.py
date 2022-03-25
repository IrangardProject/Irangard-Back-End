from django.test import TestCase
from ..models import *

class UserTestCase(TestCase):

    def setUp(self):
        
        User.objects.create(
            email = "ghazal@gmail.com",
            username = "Ghazal",
            first_name = "غزل",
            last_name = "بخشنده",
            phone_no = "09225678765",
            password = '123456',
        )

    def test_user_email(self):
        user = User.objects.get(email='Ghazal')
        self.assertEqual(user.email, 'ghazal@gmail.com')

    def test_user_phone_no(self):
        user = User.objects.get(email='ghazal@gmail.com')
        self.assertEqual(user.phone_no, '09225678765')
    
    def test_user_password(self):
        user = User.objects.get(email='Ghazal')
        self.assertEqual(user.password, '123456')