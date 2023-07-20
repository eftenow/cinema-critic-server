from django.db import models


class Genre(models.Model):
    CHOICES = (
        ('action', 'Action'),
        ('animation', 'Animation'),
        ('adventure', 'Adventure'),
        ('comedy', 'Comedy'),
        ('crime', 'Crime'),
        ('drama', 'Drama'),
        ('sci-fi', 'Sci-Fi'),
        ('fantasy', 'Fantasy'),
        ('horror', 'Horror'),
        ('mystery', 'Mystery'),
        ('romance', 'Romance'),
    )
    name = models.CharField(
        max_length=20,
        choices=CHOICES,
        unique=True
    )

    def __str__(self):
        return self.name