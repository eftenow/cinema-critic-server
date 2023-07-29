from rest_framework import serializers

from cinema_critic_server.common.models import Genre
from cinema_critic_server.content.models import Movie


class MovieReadSerializer(serializers.ModelSerializer):
    genres = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ['id', 'name', 'year', 'rating', 'director', 'stars', 'visits', 'genres', 'trailer', 'image', 'length',
                  'created_at', 'slug', 'description']


class MovieCreateEditSerializer(serializers.ModelSerializer):
    genres = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Genre.objects.all()
    )

    class Meta:
        model = Movie
        fields = ['id', 'name', 'year', 'director', 'stars', 'genres', 'trailer', 'image', 'length', 'description']


class SearchMovieSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default='movie', read_only=True)
    """
    The only reason I include the type field here is because my front-end uses
    the type of the returned object in order to be able to further redirect to
    the corresponding movie/series. There was no easy work around this other
    than simply including it in the serializers of the only 1 views that uses
    it (SearchView). The same goes for SearchSeriesSerializer.
    """
    class Meta:
        model = Movie
        fields = ['id', 'name', 'image', 'type']


class SearchSeriesSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default='series', read_only=True)

    class Meta:
        model = Movie
        fields = ['id', 'name', 'image', 'type']
