from django.db import models
from accounts.models import User
from places.models import Place

class Experience(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True, null=True)
    likeNumber = models.IntegerField(default=0)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='experiences')
    
# class Like(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
#     experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='likes')
    
    