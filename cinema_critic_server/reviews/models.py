from django.contrib.auth import get_user_model
from django.db import models

from cinema_critic_server.movies.models import Movie
from cinema_critic_server.series.models import Series

UserModel = get_user_model()
class Review(models.Model):
    review_title = models.CharField(max_length=30)
    review_description = models.TextField(
        blank=True,
        null=True,
    )
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, blank=True)
    series = models.ForeignKey(Series, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    rating = models.IntegerField()