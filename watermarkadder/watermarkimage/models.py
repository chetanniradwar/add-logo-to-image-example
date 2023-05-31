from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from .enums import ROLES


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=ROLES)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Image(models.Model):
    user = models.ForeignKey(UserProfile, null=True, blank=True, on_delete=models.SET_NULL)
    original_link = models.URLField()
    edited_link = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


