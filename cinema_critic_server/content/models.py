from _decimal import Decimal

from django.contrib.contenttypes.models import ContentType
from django.core import validators
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone

from cinema_critic_server.common.models import Genre
from cinema_critic_server.content.validators import validate_current_year


class Content(models.Model):
    name = models.CharField(max_length=40, validators=[validators.MinLengthValidator(2)])
    year = models.IntegerField(null=False, blank=False,
                               validators=[validators.MinValueValidator(1900), validate_current_year])
    rating = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True,
                                 validators=[validators.MinValueValidator(1),
                                             validators.MaxValueValidator(10)])
    director = models.CharField(max_length=30, validators=[validators.MinLengthValidator(2)])
    stars = models.CharField(max_length=60, validators=[validators.MinLengthValidator(2)])
    visits = models.IntegerField(blank=True, null=True, default=0)
    slug = models.SlugField(unique=True, editable=False, null=True)
    genres = models.ManyToManyField(Genre)
    trailer = models.URLField()
    image = models.URLField(null=False, blank=False)
    length = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now, null=True, blank=True)

    class Meta:
        abstract = True

    def update_rating(self):
        from cinema_critic_server.reviews.models import Review
        content_type = ContentType.objects.get_for_model(self.__class__)
        filtered_reviews = Review.objects.filter(content_type=content_type, object_id=self.id)

        ratings = [Decimal(review.rating) for review in filtered_reviews]
        print(f'Ratings: {ratings}')
        if ratings:
            average = sum(ratings) / Decimal(len(ratings))

            self.rating = Decimal(average)
        else:
            self.rating = None
        self.save()

    def update_visits_count(self):
        self.visits += 1
        self.save()


class Movie(Content):
    pass


class Series(Content):
    seasons = models.IntegerField(null=False, blank=False, validators=[validators.MinValueValidator(1)])
    episodes = models.IntegerField(null=False, blank=False, validators=[validators.MinValueValidator(1)])
