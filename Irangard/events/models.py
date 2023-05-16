from datetime import datetime, timezone
from django.db import models
from django.template.loader import render_to_string
from Irangard import settings
from accounts.models import User
from emails.models import EmailQueue
from utils.constants import EVENT_CATEGORIES, EVENT_TYPES
from utils.constants import StatusMode


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
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    views = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=2, choices=StatusMode.choices, default=StatusMode.PENDING)
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
                email = EmailQueue.objects.create(email_title='رویداد جدید در ایرانگرد منتظر شماست !',
                                                  email_body=self.get_tour_notification_email_template(user),
                                                  sender=settings.EMAIL_HOST_USER,
                                                  receiver=user.email)
                email.save()
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
    
    @property
    def is_expired(self):
        end_datetime = datetime.combine(self.end_date, 
                                    datetime.min.time()).replace(tzinfo=timezone.utc)
        current_datetime = datetime.now(timezone.utc)
        return (current_datetime - end_datetime).days > 0
            
    @property
    def recommendation_rate(self):
        if self.is_expired:
            return None
        
        date_created = datetime.combine(self.date_created, 
                                    datetime.min.time()).replace(tzinfo=timezone.utc)
        current_datetime = datetime.now(timezone.utc)
        start_date = datetime.combine(self.start_date, 
                                    datetime.min.time()).replace(tzinfo=timezone.utc)
        
        try:    
            view_rate = (self.views / (current_datetime - date_created).days)
        except ZeroDivisionError as zero_div:
            view_rate = 0
        
        days_to_start_rate = (start_date - current_datetime).days
        
        return view_rate - days_to_start_rate


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
