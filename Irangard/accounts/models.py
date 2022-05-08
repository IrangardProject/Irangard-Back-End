from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(
        upload_to='images/users/', blank=True, null=True)
    phone_no = models.CharField(max_length=11, null=True, blank=True)
    is_special = models.BooleanField(default=False, blank=True)
    about_me = models.TextField(null=True, blank=True)
    following_number = models.IntegerField(default=0)
    follower_number = models.IntegerField(default=0)
    is_admin = models.BooleanField(default=False, blank=True)
    

class SpecialUser(User):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='special_users')

class Verification(models.Model):
    email = models.EmailField(primary_key=True)
    username =  models.CharField(max_length=255)
    token = models.CharField(max_length=6)
    create_time = models.DateTimeField(auto_now_add=True)

class Token(models.Model):
    uid = models.CharField(primary_key=True, max_length=100)
    token = models.CharField(max_length=100)
    create_time = models.DateTimeField(auto_now_add=True)

class StagedPayments(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staged_payments_info')
    transaction_id = models.CharField(max_length=50)
    order_id = models.CharField(max_length=50)
