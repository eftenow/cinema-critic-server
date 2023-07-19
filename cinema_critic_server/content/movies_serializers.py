from rest_framework import serializers

from cinema_critic_server.common.models import Genre
from cinema_critic_server.common.serializers import GenreSerializer
from cinema_critic_server.movies.models import Movie


class MovieReadSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ['id', 'name', 'year', 'rating', 'director', 'stars', 'visits', 'genres', 'trailer', 'image', 'length',
                  'created_at']


class MovieCreateEditSerializer(serializers.ModelSerializer):
    genres = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Genre.objects.all()
    )

    class Meta:
        model = Movie
        fields = ['id', 'name', 'year', 'director', 'stars', 'genres', 'trailer', 'image', 'length']
