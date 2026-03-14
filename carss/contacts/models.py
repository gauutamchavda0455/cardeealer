from django.db import models
from django.utils import timezone


class Contact(models.Model):
    listing = models.CharField(max_length=255)
    listing_id = models.IntegerField()
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    message = models.TextField(blank=True)
    contact_date = models.DateField(default=timezone.now, blank=True)
    user_id = models.IntegerField(blank=True)

    def __str__(self):
        return self.name
