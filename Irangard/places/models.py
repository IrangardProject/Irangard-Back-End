from django.db import models
from accounts.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Place(models.Model):
    PlaceTypes = [
        ('0', "رستوران ها و کافه ها"),
        ('1', "اقامتگاه ها"),
        ('2', "مراکز تفریحی"),
        ('3', "جاذبه های دیدنی"),
    ]
    place_type = models.CharField(max_length=20, choices=PlaceTypes)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    rate = models.DecimalField(
        max_digits=2, decimal_places=1, default=5, blank=True)
    rate_no = models.IntegerField(default=0, blank=True)
    is_free = models.BooleanField(default=False, blank=True)
    added_by = models.ForeignKey(
        User, related_name='added_places', on_delete=models.DO_NOTHING)
    date_created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, related_name='owned_places', on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return f'{self.title} => {self.place_type}'

    def is_adimn_or_owner(self, user):
        return self.owner == user or user.is_admin
    
    def update_rate(self):
        rates = self.rates.all()
        self.rate_no = len(rates)
        self.rate = round(sum(
            [rate_obj.rate for rate_obj in rates]) / self.rate_no, 1)
        self.save()


class Image(models.Model):
    place = models.ForeignKey(
        Place, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=f'images/places')
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.pk} {self.place}'


class Rate(models.Model):
    place = models.ForeignKey(
        Place, on_delete=models.CASCADE, related_name='rates')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='rates')
    rate = models.DecimalField(
        max_digits=2, decimal_places=1, default=5, 
        validators=[MinValueValidator(0), MaxValueValidator(5)])

    def __str__(self):
        return f"{user.username} rated {self.rate} to {self.place.title}"


class Tag(models.Model):
    place = models.ForeignKey(
        Place, on_delete=models.CASCADE, related_name='tags')
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.place.title} {self.name}"


class Contact(models.Model):
    place = models.OneToOneField(
        Place, on_delete=models.CASCADE, related_name='contact')
    x_location = models.DecimalField(max_digits=15, decimal_places=10)
    y_location = models.DecimalField(max_digits=15, decimal_places=10)
    province = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    instagram = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.place.title} {self.province} {self.city}"


class Location(models.Model):
    contact = models.OneToOneField(
        Contact, on_delete=models.CASCADE, related_name='location') 
    x = models.DecimalField(max_digits=6, decimal_places=3)
    y = models.DecimalField(max_digits=6, decimal_places=3)

    def __str__(self):
        return f"{self.contact.place.title}: {self.x}, {self.y}"


class Feature(models.Model):
    place = models.ForeignKey(
        Place, on_delete=models.CASCADE, related_name='features')
    title = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.place.title} {self.title}"


class Room(models.Model):
    place = models.ForeignKey(
        Place, on_delete=models.CASCADE, related_name='rooms')
    room_type = models.CharField(max_length=255) #mishe choices gozasht
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=3)

    def __str__(self):
        return f"{self.place.title} {self.room_type}"


class Optional(models.Model):
    place = models.ForeignKey(
        Place, on_delete=models.CASCADE, related_name='optional_costs')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=3)

    def __str__(self):
        return f"{self.place.title} {self.title}"

class Hours(models.Model):
    weekdays = [
        ('0', "Saturday"),
        ('1', "Sunday"),
        ('2', "Monday"),
        ('3', "Tuesday"),
        ('4', "Wednesday"),
        ('5', "Thursday"),
        ('6', "Friday")
    ]
    contact = models.ForeignKey(
        Contact, on_delete=models.CASCADE, related_name='working_hours')
    weekday = models.CharField(max_length=255, choices=weekdays)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    all_day = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.place.title}: {self.day} {self.start_time}-{self.end_time}"
    

