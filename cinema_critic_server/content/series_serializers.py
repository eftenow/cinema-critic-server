from rest_framework import serializers

from cinema_critic_server.common.models import Genre
from cinema_critic_server.common.serializers import GenreSerializer
from cinema_critic_server.series.models import Series


class SeriesReadSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Series
        fields = ['id', 'name', 'year', 'rating', 'director', 'stars', 'visits', 'genres', 'trailer', 'image', 'length',
                  'seasons', 'episodes', 'created_at']


class SeriesCreateEditSerializer(serializers.ModelSerializer):
    genres = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Genre.objects.all()
    )

    class Meta:
        model = Series
        fields = ['id', 'name', 'year', 'director', 'stars', 'genres', 'trailer', 'image', 'length',
                  'seasons', 'episodes']
