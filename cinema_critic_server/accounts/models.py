from django.core import validators
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from cinema_critic_server.accounts.managers import AppUserManager
from cinema_critic_server.accounts.validators import name_contains_only_letters
from cinema_critic_server.content.models import Movie
from cinema_critic_server.content.models import Series


class AppUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
        max_length=20,
        validators=[validators.MinLengthValidator(2)],
    )
    username = models.CharField(
        unique=True,
        max_length=20,
        validators=[validators.MinLengthValidator(2)],
    )
    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"

    objects = AppUserManager()


class Profile(models.Model):
    MAX_NAME_LEN = 30
    MIN_NAME_LEN = 2
    CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Do not show', 'Do not show'),
    )

    first_name = models.CharField(
        max_length=MAX_NAME_LEN,
        validators=[validators.MinLengthValidator(MIN_NAME_LEN), name_contains_only_letters],
        null=True,
        blank=True,
    )

    last_name = models.CharField(
        max_length=MAX_NAME_LEN,
        validators=[validators.MinLengthValidator(MIN_NAME_LEN), name_contains_only_letters],
        null=True,
        blank=True,
    )

    profile_picture = models.URLField(
        null=True,
        blank=True,
    )
    gender = models.CharField(
        choices=CHOICES,
        max_length=15,
        null=True,
        blank=True,
    )

    city = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )

    country = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )

    description = models.TextField(
        max_length=100,
        null=True,
        blank=True,
    )
    user = models.OneToOneField(
        AppUser,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='profile'
    )
    bookmarked_movies = models.ManyToManyField(Movie, related_name='bookmarked_by', blank=True)
    bookmarked_series = models.ManyToManyField(Series, related_name='bookmarked_by', blank=True)

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        else:
            return self.user.username
