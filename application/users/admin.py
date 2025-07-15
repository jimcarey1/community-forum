"""
This module registers the custom User model with the Django admin site,
allowing administrators to manage user accounts.
"""
from django.contrib import admin
from .models import User
# Register your models here.

admin.site.register(User)