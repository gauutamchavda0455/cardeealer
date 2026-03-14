from django.db import models
from django.utils import timezone


class Advisor(models.Model):
    name = models.CharField(max_length=200)
    # needs pillow to use imagefield
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    description = models.TextField(blank=True)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    is_mvp = models.BooleanField(default=False)
    hire_date = models.DateField(default=timezone.now, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # for admin area primary column
    def __str__(self):
        return self.name
