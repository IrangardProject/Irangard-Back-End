from django.db import models
from accounts.models import User
from tours.models import Tour
from events.models import Event
from places.models import Place


class TourSuggestion(models.Model):
    sender = models.ForeignKey(
        User, related_name='tours_suggested_by', on_delete=models.CASCADE)
    receiver = models.ForeignKey(
        User, related_name='tours_suggested_to', on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, related_name='suggestions', 
                            on_delete=models.CASCADE)
    text = models.CharField(max_length=255, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return f"{self.sender} suggests {self.tour.title} to {self.receiver}"


class EventSuggestion(models.Model):
    sender = models.ForeignKey(
        User, related_name='events_suggested_by', on_delete=models.CASCADE)
    receiver = models.ForeignKey(
        User, related_name='events_suggested_to', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name='suggestions',
                            on_delete= models.CASCADE)
    text = models.CharField(max_length=255, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return f"{self.sender} suggests {self.event.title} to {self.receiver}"
    
class PlaceSuggestion(models.Model):
    sender = models.ForeignKey(
        User, related_name='places_suggested_by', on_delete=models.CASCADE)
    receiver = models.ForeignKey(
        User, related_name='places_suggested_to', on_delete=models.CASCADE)
    place = models.ForeignKey(Place, related_name='suggestions',
                            on_delete=models.CASCADE)
    text = models.CharField(max_length=255, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return f"{self.sender} suggests {self.place.title} to {self.receiver}"
    