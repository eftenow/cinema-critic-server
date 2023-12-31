from itertools import chain

from django.db.models import Q
from django.db.models import F
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from cinema_critic_server.content.custom_mixins.filtration_mixin import FilterSortMixin, ContentSortMixin
from cinema_critic_server.content.models import Movie, Series
from cinema_critic_server.content.pagination import MoviesSeriesPaginator
from cinema_critic_server.content.serializers.serialiers_search import SearchSeriesSerializer, SearchMovieSerializer
from cinema_critic_server.content.serializers.serializers_content import ContentSerializer
from cinema_critic_server.content.serializers.serializers_movies import MovieCreateEditSerializer, MovieReadSerializer
from cinema_critic_server.content.serializers.serializers_series import SeriesCreateEditSerializer, SeriesReadSerializer

""""Content (Movies + Series) views"""

class ContentListView(ContentSortMixin, FilterSortMixin, ListAPIView):
    serializer_class = ContentSerializer
    pagination_class = MoviesSeriesPaginator

    def get_queryset(self):
        movie_queryset = Movie.objects.all()
        series_queryset = Series.objects.all()

        # the get_filtered_sorted_queryset comes from the custom mixin that is inherited
        filtered_sorted_movies = self.get_filtered_sorted_queryset(movie_queryset)
        filtered_sorted_series = self.get_filtered_sorted_queryset(series_queryset)

        filtered_content = list(chain(list(filtered_sorted_movies), list(filtered_sorted_series)))

        sort_param = self.request.query_params.get('sort')
        sorted_and_filtered_content = self.sort_all_content(filtered_content, sort_param)

        return sorted_and_filtered_content


class PopularContentView(APIView):

    def get(self, request, *args, **kwargs):
        top_movies = Movie.objects.all().annotate(content_type=F('type')).order_by('-visits')[:5]
        top_series = Series.objects.all().annotate(content_type=F('type')).order_by('-visits')[:5]

        combined = list(chain(top_movies, top_series))
        combined_sorted = sorted(combined, key=lambda content: content.visits, reverse=True)[:5]

        # You will need to serialize these objects to convert them to JSON response
        serializer_data = ContentSerializer(combined_sorted, many=True).data

        return Response(serializer_data)


""""Movie views"""


class MovieListCreateView(FilterSortMixin, ListCreateAPIView):
    queryset = Movie.objects.all()
    pagination_class = MoviesSeriesPaginator
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        sorted_and_filtered_queryset = self.get_filtered_sorted_queryset(queryset)
        return sorted_and_filtered_queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MovieCreateEditSerializer
        return MovieReadSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class MovieDetailsEditDeleteView(RetrieveUpdateDestroyAPIView):
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

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        user_is_administrator = request.user.groups.filter(name='Administrator').exists()

        if instance.creator != request.user and not user_is_administrator:
            return Response({"detail": "Not authorized to update this movie"}, status=status.HTTP_403_FORBIDDEN)

        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save()


""""Series views"""


class SeriesListCreateView(FilterSortMixin, ListCreateAPIView):
    queryset = Series.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SeriesCreateEditSerializer
        return SeriesReadSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        sorted_and_filtered_queryset = self.get_filtered_sorted_queryset(queryset)
        return sorted_and_filtered_queryset

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class SeriesDetailsEditDeleteView(RetrieveUpdateDestroyAPIView):
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

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        user_is_administrator = request.user.groups.filter(name='Administrator').exists()

        if instance.creator != request.user and not user_is_administrator:
            return Response({"detail": "Not authorized to update this series"}, status=status.HTTP_403_FORBIDDEN)

        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save()


"""Search view"""


class SearchView(APIView):
    def get(self, request):
        query = request.query_params.get('q', None)

        if not query:
            return Response({"error": "No search text."}, status=400)
        """
        I cannot use directly the base class 'Content', because it is an abstract class
        and an abstract class can't be instantiated nor use built-in functionalities(managers),
        such as the 'objects' manager,which in this case is necessary here in order to retrieve
        the searched objects. Instead I use both 'Movie' and 'Series' classes separately.
        """

        movie_queryset = Movie.objects.filter(Q(name__icontains=query))
        series_queryset = Series.objects.filter(Q(name__icontains=query))

        movie_serializer = SearchMovieSerializer(movie_queryset, many=True)
        series_serializer = SearchSeriesSerializer(series_queryset, many=True)

        results = (movie_serializer.data + series_serializer.data)[:6]

        return Response(results)
