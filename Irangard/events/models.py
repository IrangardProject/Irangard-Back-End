from django.db import models
from accounts.models import User

class Event(models.Model):
    EVENT_TYPES = [
        ('0', 'همایش'),
        ('1', 'نمایشگاه'),
        ('2', 'نمایش'),
        ('3', 'کنسرت یا اجرا'),
        ('4', 'جشنواره'),
        ('5', 'مسابقه'),
        ('6', 'کنفرانس'),
        ('7', 'سمینار'),
        ('8', 'مجمع'),
        ('9', 'جشن'),
        ('10', 'مراسم'),
        ('11', 'سایر')
    ]
    
    EVENT_CATEGORIES = [
        ('0', 'هنری'),
        ('1', 'علمی'),
        ('2', 'فرهنگی'),
        ('3', 'ورزشی'),
        ('4', 'سیاسی'),
        ('5', 'اجتماعی'),
        ('6', 'مذهبی'),
        ('7', 'تجاری'),
        ('8', 'سایر'),
    ]
    
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


