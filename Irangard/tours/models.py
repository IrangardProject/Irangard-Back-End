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
    bookers = models.ManyToManyField(User, blank=True, related_name='tours')
    total_revenue = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    def __str__(self):
        return self.title

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

