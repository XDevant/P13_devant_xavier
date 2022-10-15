from django.db import models
from django.contrib.auth.models import User
from lettings.models import Address as Add


class Letting(models.Model):
    title = models.CharField(max_length=256)
    address = models.OneToOneField(Add, on_delete=models.CASCADE, related_name='old_address')

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile_user')
    favorite_city = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return self.user.username
