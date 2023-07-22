from itertools import chain

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView

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
        movies = Movie.objects.all()
        series = Series.objects.all()

        # using "chain" instead of movies + series, because they're of type QuerySet and do not support the '+' operator
        content = list(chain(movies, series))
        content.sort(key=lambda x: x.created_at, reverse=True)

        return content


""""Movie views"""


class MovieListCreateView(FilterSortMixin, ListCreateAPIView):
    queryset = Movie.objects.all()
    pagination_class = MoviesSeriesPaginator

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


""""Series views"""


class SeriesListCreateView(FilterSortMixin, ListCreateAPIView):
    queryset = Series.objects.all()

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
