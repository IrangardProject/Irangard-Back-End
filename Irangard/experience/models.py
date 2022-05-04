from django.db import models
from accounts.models import User
from places.models import Place

class Experience(models.Model):
    title = models.CharField(max_length=255)
    image = models.CharField()
    like_number = models.IntegerField(default=0)
    comment_number = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    summary = models.TextField(blank=True, null=True, max_length=500)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='experiences')
    date_created = models.CharField(max_length=255)
    
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='likes')
    
    