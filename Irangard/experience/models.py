from django.db import models
from accounts.models import User
from places.models import Place
from cloudinary.models import CloudinaryField

class Experience(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to=f'images/experiences', null=True, blank=True)
    like_number = models.IntegerField(default=0)
    comment_number = models.IntegerField(default=0)
    rate = models.IntegerField(default=5)
    summary = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    body = models.TextField(blank=True, null=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='experiences')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiences')
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes_user')
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='likes_experience')

class Comment(models.Model):
    experience = models.ForeignKey(
        Experience, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    parent = models.OneToOneField('Comment', on_delete=models.CASCADE, 
                        related_name='reply', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    def __str__(self):
        return f"{self.experience.title} {self.user.username}"

    def is_owner(self, user):
        return self.user == user
