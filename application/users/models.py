from django.contrib.auth.models import AbstractUser, UserManager

class CustomUserManager(UserManager):
    def _create_user_object(self, username=None, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError('Username must be set.')
        if not email:
            raise ValueError('Email must be set.')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        return user
    
    def _create_user(self, username, email, password, **extra_fields):
        user = self._create_user_object(username, email, password, **extra_fields)
        user.save()
        return user
    
    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)
    
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)

class User(AbstractUser):

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = CustomUserManager()

    class Meta:
        pass