from django.contrib.auth import get_user_model
from django.db import models

from cinema_critic_server.movies.models import Movie
from cinema_critic_server.series.models import Series

UserModel = get_user_model()


class MovieReview(models.Model):
    review_title = models.CharField(max_length=30)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.TextField(
        blank=True,
        null=True
    )
    rating = models.IntegerField()

    # Add other fields for the movie review as needed


class SeriesReview(models.Model):
    review_title = models.CharField(max_length=30)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    content = models.TextField(
        blank=True,
        null=True
    )
    rating = models.IntegerField()
