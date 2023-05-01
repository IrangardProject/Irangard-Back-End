from django.core.mail import EmailMessage
from django.db import models
from django.template.loader import render_to_string

from Irangard import settings
from accounts.models import User
from utils.constants import EVENT_CATEGORIES, EVENT_TYPES

class Event(models.Model):
    event_type = models.CharField(
        max_length=20, choices=EVENT_TYPES, default='11')
    event_category = models.CharField(
        max_length=20, choices=EVENT_CATEGORIES, default='8')
    title = models.CharField(max_length=255)
    organizer = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    x_location = models.DecimalField(max_digits=20, decimal_places=15)
    y_location = models.DecimalField(max_digits=20, decimal_places=15)
    province = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    added_by = models.ForeignKey(
        User, related_name='events',
        on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=255)
    is_free = models.BooleanField(default=False, blank=True)
    website = models.CharField(max_length=255)
    phone = models.CharField(max_length=11, blank=True, null=True)
    # cost = models.IntegerField(default=0)
    # have_capacity = models.BooleanField(default=False, blank=True)
    # capacity = models.IntegerField(default=-1)
    # remaining = models.IntegerField(default=0)
    
    
    def __str__(self):
        return self.title

    def get_tour_notification_email_template(self, user):
        template = render_to_string('email-notification.html',
                                    {
                                        'tour': self,
                                        'username': user.full_name,
                                    })
        return template

    def get_related_users(self):
        """
            related users are those who have common categories with this tour categories in their favorites
        """
        all_users = User.objects.all()
        related_users = []
        for user in all_users:
            if self.event_type in user.favorite_event_types:
                related_users.append(user)
        return related_users

    def send_email_to_related_users(self):
        related_users = self.get_related_users()
        try:
            for user in related_users:
                email = EmailMessage('رویداد جدید در ایرانگرد منتظر شماست !',
                                     self.get_tour_notification_email_template(user),
                                     settings.EMAIL_HOST_USER,
                                     [user.email]
                                     )
                email.content_subtype = "html"
                email.fail_silently = False
                email.send()
                print(f"##### email sent to user {user.username}, id = {user.id}")
        except TimeoutError as t:
            print("timeout error")
            return False
        except Exception as e:
            print(e)
            return False
        else:
            return True

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        is_created = self.pk is None
        super(Event, self).save(force_insert=False, force_update=False, using=None,
             update_fields=None)
        if is_created:
            self.send_email_to_related_users()

class Tag(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name='tags')
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.event.title} {self.name}"
        

class Image(models.Model):
    event = models.ForeignKey(
        Event, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=f'images/events')
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.pk} {self.event}'
