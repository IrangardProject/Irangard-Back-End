from django.db import models
from accounts.models import User, SpecialUser



class Tour(models.Model):
    title = models.CharField(max_length=255)
    cost = models.IntegerField(default=0)
    capacity = models.IntegerField(default=0)
    remaining = models.IntegerField(default=0)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    owner = models.ForeignKey("accounts.SpecialUser",related_name="tours",on_delete=models.CASCADE)

    def __str__(self):
        return self.title

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
    expire_data = models.DateTimeField()
    code = models.CharField(max_length=255)
    tour = models.ForeignKey(
        'Tour', related_name='discount_codes', on_delete=models.CASCADE)

    def __str__(self):
        return self.tour.title +": " + self.code

