from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)

    # Define a related_name for groups and user_permissions to avoid clashes
    groups = models.ManyToManyField('auth.Group', related_name='customuser_set')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='customuser_set')

    # Set the 'USERNAME_FIELD' to 'email'
    USERNAME_FIELD = 'email'

    # Exclude 'email' from 'REQUIRED_FIELDS' because it's the 'USERNAME_FIELD'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.username  # You can change this to return any user identifier
