from django.contrib import admin
from .models import Chat, MessageRoom, UserInRoom, Message

# Register your models here.
admin.site.register(Chat)
admin.site.register(MessageRoom)
admin.site.register(UserInRoom)
admin.site.register(Message)
