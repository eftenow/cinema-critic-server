from django.db.models import Q
from itertools import chain
from rest_framework import generics
from rest_framework.response import Response

from cinema_critic_server.common.models import Genre
from cinema_critic_server.common.serializers import GenreSerializer
from cinema_critic_server.content.models import Movie, Series
from cinema_critic_server.content.serializers.serializers_movies import MovieReadSerializer
from cinema_critic_server.content.serializers.serializers_series import SeriesReadSerializer


class ContentSearchListView(generics.ListAPIView):

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        movie_queryset = Movie.objects.filter(Q(name__icontains=query))
        series_queryset = Series.objects.filter(Q(name__icontains=query))
        queryset_combined = list(chain(movie_queryset, series_queryset))
        return queryset_combined

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        movie_queryset = [q for q in queryset if isinstance(q, Movie)]
        series_queryset = [q for q in queryset if isinstance(q, Series)]
        movie_serializer = MovieReadSerializer(movie_queryset, many=True)
        series_serializer = SeriesReadSerializer(series_queryset, many=True)
        return Response({
            'movies': movie_serializer.data,
            'series': series_serializer.data,
        })


class GenresListView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
