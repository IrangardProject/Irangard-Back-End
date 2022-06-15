from django.db import models
from accounts.models import User
# Create your models here.


class Chat(models.Model):
    sender = models.ForeignKey(
        User, related_name='send_chats', on_delete=models.CASCADE)
    receiver = models.ForeignKey(
        User, related_name='received_chats', on_delete=models.CASCADE)
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    room_name = models.CharField(max_length=250)
