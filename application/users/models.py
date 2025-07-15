"""
This module defines the custom user model and manager for the application.
"""
from django.contrib.auth.models import AbstractUser, UserManager

class CustomUserManager(UserManager):
    """
    Custom user manager that extends Django's default UserManager.
    Provides methods for creating regular users and superusers.
    """
    def _create_user_object(self, username=None, email=None, password=None, **extra_fields):
        """
        Helper method to create a user object without saving it to the database.
        """
        if not username:
            raise ValueError('Username must be set.')
        if not email:
            raise ValueError('Email must be set.')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        return user
    
    def _create_user(self, username, email, password, **extra_fields):
        """
        Helper method to create and save a user to the database.
        """
        user = self._create_user_object(username, email, password, **extra_fields)
        user.save()
        return user
    
    def create_user(self, username, email=None, password=None, **extra_fields):
        """
        Creates and saves a regular user with the given username, email, and password.
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)
    
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given username, email, and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    """
    Custom User model that extends Django's AbstractUser.
    Uses CustomUserManager as its manager.
    """
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = CustomUserManager()

    class Meta:
        pass