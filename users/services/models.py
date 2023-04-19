from django.db import models
from django.contrib.auth.models import User

from neighborhood.models import Neighborhood


class Business(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="businesses")
    neighborhood = models.ForeignKey(
        Neighborhood, on_delete=models.CASCADE, related_name="businesses"
    )
    email = models.EmailField(max_length=50, blank=True)
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
