from django.db import models
from django.utils import timezone


class Contact(models.Model):
    listing = models.CharField(max_length=255)
    listing_id = models.IntegerField()
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    contact_date = models.DateField(default=timezone.now, blank=True)
    user_id = models.IntegerField(blank=True, null=True)

    def __str__(self):
        """Return a more descriptive string representation"""
        user_type = "Registered" if self.user_id and self.user_id != 0 else "Guest"
        return f"{self.name} - {self.listing} ({user_type})"

    class Meta:
        """Meta class for additional model configuration"""
        verbose_name = "Test Drive Booking"
        verbose_name_plural = "Test Drive Bookings"
        ordering = ['-contact_date', '-id']
