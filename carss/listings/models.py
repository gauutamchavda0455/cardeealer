from django.db import models
from django.utils import timezone
from advisors.models import Advisor


class Listing(models.Model):
    advisor = models.ForeignKey(Advisor, on_delete=models.CASCADE)
    vin = models.CharField(max_length=17)
    condition = models.CharField(max_length=4)
    body_style = models.CharField(max_length=50)
    year = models.IntegerField()
    make = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    price = models.IntegerField()
    color = models.CharField(max_length=10)
    interior_color = models.CharField(max_length=10)
    drivetrain = models.CharField(max_length=10)
    transmission = models.CharField(max_length=10)
    fuel = models.CharField(max_length=10)
    mileage = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/')
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    is_published = models.BooleanField(default=True)
    list_date = models.DateTimeField(default=timezone.now, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # for admin area primary column
    def __str__(self):
        primary_column = str(self.year) + " " + self.make + \
            " " + self.model + " " + self.color
        return primary_column
