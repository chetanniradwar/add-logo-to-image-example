from django.contrib import admin

# Register your models here.
from .models import UserProfile, Image


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'original_link', 'edited_link')
