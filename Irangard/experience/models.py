from django.db import models
from accounts.models import User
from places.models import Place
from cloudinary.models import CloudinaryField

class Experience(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to=f'images/experiences')
    like_number = models.IntegerField(default=0)
    comment_number = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    rate = models.IntegerField(default=0)
    summary = models.TextField(blank=True, null=True)
    date_created = models.CharField(max_length=255)
    body = models.TextField(blank=True, null=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='experiences')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiences')
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='likes')