from django.db import models

from utils.constants import EMAIL_STATES

"""
email = EmailMessage('تور جدید در ایرانگرد منتظر شماست !',
                                     self.get_tour_notification_email_template(user),
                                     settings.EMAIL_HOST_USER,
                                     [user.email]
                                     )
"""

class EmailQueue(models.Model):
    email_title = models.CharField(max_length=256)
    email_body = models.TextField()
    sender = models.EmailField()
    receiver = models.EmailField()
    state = models.CharField(max_length=2, choices=EMAIL_STATES, default='0')
