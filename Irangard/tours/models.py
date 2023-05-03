import datetime
import time

from django.core.mail import EmailMessage
from django.db import models
from django.utils.timezone import utc

from Irangard import settings
from accounts.models import User, SpecialUser
from django.template.loader import render_to_string

from emails.models import EmailQueue
from utils.constants import TOUR_TYPES


class Tour(models.Model):

    tour_type = models.CharField(max_length=20, choices=TOUR_TYPES,
                                default='10')
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to=f'images/tours', blank=True, null=True)
    cost = models.IntegerField(default=0)
    capacity = models.IntegerField(default=0)
    remaining = models.IntegerField(default=0)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    owner = models.ForeignKey("accounts.SpecialUser",related_name="tours",on_delete=models.CASCADE)
    bookers = models.ManyToManyField(User, blank=True, related_name='tours')
    total_revenue = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.title

    @property
    def recommendation_rate(self):
        if self.is_expired:
            return None
        try:
            register_rate = (self.bookers.count() / (datetime.datetime.utcnow().replace(tzinfo=utc) - self.date_created ).days )
        except ZeroDivisionError as zero_div:
            register_rate = 0
        tour_leader_sells_count = 0
        for tour in Tour.objects.filter(owner=self.owner):
            tour_leader_sells_count += tour.bookers.count()
        tour_leader_rate = self.owner.user.follower_number + tour_leader_sells_count + Tour.objects.filter(owner=self.owner).count()
        days_to_start_rate = (self.start_date - datetime.datetime.utcnow().replace(tzinfo=utc)).days
        print(f"{self.title} : register rate = {register_rate}, tour leader rate = {tour_leader_rate}, days to start = "
              f"{days_to_start_rate}, overall = {register_rate + tour_leader_rate - days_to_start_rate}")
        return register_rate + tour_leader_rate - days_to_start_rate

    @property
    def is_expired(self):
        return (datetime.datetime.utcnow().replace(tzinfo=utc) - self.end_date).days > 0

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
            if self.tour_type in user.favorite_tour_types:
                related_users.append(user)
        return related_users

    def send_email_to_related_users(self):
        related_users = self.get_related_users()
        try:
            for user in related_users:
                email = EmailQueue.objects.create(email_title='تور جدید در ایرانگرد منتظر شماست !' ,
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
        super(Tour, self).save(force_insert=False, force_update=False, using=None,
             update_fields=None)
        if is_created :
            self.send_email_to_related_users()

    def booked(self, user):
        return self.bookers.filter(id=user.id).exists()

    def update_remaining(self):
        self.remaining = self.capacity - self.bookers.count()
        self.save()

    def update_revenue(self, amount):
        self.total_revenue += amount
        self.save()
    
    def withdraw(self, amount):
        self.total_revenue -= amount
        self.save()

class Transaction(models.Model):
    sender = models.ForeignKey(
        'accounts.User', related_name='transactions', null=True, on_delete=models.SET_NULL)
    cost = models.IntegerField(default=0)
    date = models.DateTimeField()
    tour = models.ForeignKey('Tour',related_name='transactions',on_delete=models.CASCADE)

    def __str__(self):
        return self.sender.username +": " + self.tour.title

class DiscountCode(models.Model):
    off_percentage = models.IntegerField(default=0)
    expire_date = models.DateTimeField()
    code = models.CharField(max_length=255)
    tour = models.ForeignKey(
        'Tour', related_name='discount_codes', on_delete=models.CASCADE)

    def __str__(self):
        return self.tour.title +": " + self.code
    
    def is_owner(self, user):
        return self.tour.owner.user == user

