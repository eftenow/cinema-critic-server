from rest_framework import serializers

from cinema_critic_server.common.models import Genre
from cinema_critic_server.content.models import Movie, Series


class SearchMovieSerializer(serializers.ModelSerializer):
    genres = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Genre.objects.all()
    )

    class Meta:
        model = Movie
        fields = ['id', 'name', 'image', 'type', 'genres', 'rating']


class SearchSeriesSerializer(serializers.ModelSerializer):
    genres = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Genre.objects.all()
    )
    class Meta:
        model = Series
        fields = ['id', 'name', 'image', 'type', 'genres', 'rating']