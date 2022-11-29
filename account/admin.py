from django.contrib import admin
from .models import Profile, Contacts

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['image', 'user']

@admin.register(Contacts)
class ContacsAdmin(admin.ModelAdmin):
    list_display = ['user_from', 'user_to']