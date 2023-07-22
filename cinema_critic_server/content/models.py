from django.core import validators
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone

from cinema_critic_server.common.models import Genre


# Create your models here.
class Content(models.Model):
    name = models.CharField(max_length=30)
    year = models.IntegerField(validators=[validators.MinValueValidator(1900)])
    rating = models.IntegerField(null=True, blank=True)
    director = models.CharField(max_length=30)
    stars = models.CharField(max_length=60)
    visits = models.IntegerField(blank=True, null=True)
    slug = models.SlugField(unique=True, editable=False, null=True)
    genres = models.ManyToManyField(Genre)
    trailer = models.URLField()
    image = models.URLField()
    length = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now, null=True, blank=True)

    class Meta:
        abstract = True


class Movie(Content):
    pass


class Series(Content):
    seasons = models.IntegerField()
    episodes = models.IntegerField()
