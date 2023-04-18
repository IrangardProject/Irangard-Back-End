from django.db import models
from accounts.models import User
# Create your models here.


class Chat(models.Model):
    
    class SenderType(models.TextChoices):
        server = 'SERVER'
        Client = 'CLIENT'
    
    sender = models.ForeignKey(
        User, related_name='send_chats', on_delete=models.CASCADE)
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    room_name = models.CharField(max_length=250)
    sender_type= models.CharField(max_length=6, choices=SenderType.choices, null=True)

class MessageRoom(models.Model):
    name = models.CharField(max_length=250)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"room name = {self.name}, owner = {self.owner}"

class UserInRoom(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(MessageRoom, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} joined room {self.room.id}"

class Message(models.Model):
    sender = models.ForeignKey(
        User, related_name='message_sender', on_delete=models.CASCADE)
    message = models.TextField()
    reciever_room = models.ForeignKey(MessageRoom, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username} send a message in room {self.reciever_room.name}'