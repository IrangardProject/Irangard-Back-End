from django.db import models
from accounts.models import User

class Event(models.Model):
    EVENT_TYPES = [
        ('0', "سایر"),
        ('1', "جشنواره"),
        ('2', "کنسرت موسیقی"),
        ('3', "مسابقه"),
        ('4', "مهمانی و دورهمی"),
    ]
    
    EVENT_CATEGORIES = [
        ('0', "سایر"),
        ('1', "خانوادگی"),
        ('2', "هنری"),
        ('3', "بیزنسی"),
        ('4', "مذهبی"),
    ]
    
    event_type = models.CharField(
        max_length=20, choices=EVENT_TYPES, default='0')
    event_category = models.CharField(
        max_length=20, choices=EVENT_CATEGORIES, default='0')
    title = models.CharField(max_length=255)
    organizer = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    x_location = models.DecimalField(max_digits=15, decimal_places=10)
    y_location = models.DecimalField(max_digits=15, decimal_places=10)
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
    # cost = models.IntegerField(default=0)
    # have_capacity = models.BooleanField(default=False, blank=True)
    # capacity = models.IntegerField(default=-1)
    # remaining = models.IntegerField(default=0)
    
    
    def __str__(self):
        return self.title

    
    

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
