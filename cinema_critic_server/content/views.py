from itertools import chain

from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from cinema_critic_server.content.custom_mixins.filtration_mixin import FilterSortMixin
from cinema_critic_server.content.models import Movie, Series
from cinema_critic_server.content.pagination import MoviesSeriesPaginator
from cinema_critic_server.content.serializers.serializers_content import ContentSerializer
from cinema_critic_server.content.serializers.serializers_movies import MovieCreateEditSerializer, MovieReadSerializer
from cinema_critic_server.content.serializers.serializers_series import SeriesCreateEditSerializer, SeriesReadSerializer

""""Movies + Series views"""


class ContentListView(FilterSortMixin, ListAPIView):
    serializer_class = ContentSerializer
    pagination_class = MoviesSeriesPaginator

    def get_queryset(self):
        movie_queryset = Movie.objects.all()
        series_queryset = Series.objects.all()

        # the get_filtered_sorted_queryset comes from the custom mixin that is inherited
        filtered_sorted_movies = self.get_filtered_sorted_queryset(movie_queryset)
        filtered_sorted_series = self.get_filtered_sorted_queryset(series_queryset)

        content = list(chain(filtered_sorted_movies, filtered_sorted_series))

        return content


""""Movie views"""


class MovieListCreateView(FilterSortMixin, ListCreateAPIView):
    queryset = Movie.objects.all()
    pagination_class = MoviesSeriesPaginator
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        return sorted(queryset, key=lambda x: x.created_at, reverse=True)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MovieCreateEditSerializer
        return MovieReadSerializer


class MovieDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    pagination_class = MoviesSeriesPaginator

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MovieReadSerializer
        return MovieCreateEditSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.update_visits_count()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


""""Series views"""


class SeriesListCreateView(FilterSortMixin, ListCreateAPIView):
    queryset = Series.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SeriesCreateEditSerializer
        return SeriesReadSerializer


class SeriesDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Series.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SeriesReadSerializer
        return SeriesCreateEditSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.update_visits_count()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
