from django.db import models

from utils.constants import EMAIL_STATES


class EmailQueue(models.Model):
    email_title = models.CharField(max_length=256)
    email_body = models.TextField()
    sender = models.EmailField()
    receiver = models.EmailField()
    state = models.CharField(max_length=2, choices=EMAIL_STATES, default='0')
