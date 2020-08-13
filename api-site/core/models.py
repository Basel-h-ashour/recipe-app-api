from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin


class UserManager(BaseUserManager):
    """manages custom made user class to override create_superuser in CLI"""

    def create_user(self, email, name, password=None, **extra_kwargs):
        """creates a new user with normal permissions"""
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """creates a new user with superuser rights"""
        user = self.create_user(email, name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """model class representing a User in our system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', ]

    def get_full_name(self):
        """returns the full name of user"""
        return self.name

    def get_short_name(self):
        """returns the short name of user"""
        return self.name

    def __str__(self):
        """returns string representation of the user"""
        return self.email


class Tag(models.Model):
    """Tag to be used for a recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
