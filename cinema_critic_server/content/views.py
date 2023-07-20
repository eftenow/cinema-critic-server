from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from cinema_critic_server.content.models import Movie, Series
from cinema_critic_server.content.movies_serializers import MovieReadSerializer, MovieCreateEditSerializer
from cinema_critic_server.content.series_serializers import SeriesCreateEditSerializer, SeriesReadSerializer


class MovieListCreateView(ListCreateAPIView):
    queryset = Movie.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MovieCreateEditSerializer
        return MovieReadSerializer


class MovieDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MovieReadSerializer
        return MovieCreateEditSerializer


#####

class SeriestListCreateView(ListCreateAPIView):
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
