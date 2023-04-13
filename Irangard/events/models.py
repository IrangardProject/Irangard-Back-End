from django.db import models


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
    
    title = models.CharField(max_length=255)
    organizer = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    x_location = models.DecimalField(max_digits=15, decimal_places=10)
    y_location = models.DecimalField(max_digits=15, decimal_places=10)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


class Tag(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name='tags')
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.event.title} {self.name}"
        

class Image(models.Model):
    evnt = models.ForeignKey(
        Event, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=f'images/events')
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.pk} {self.event}'
