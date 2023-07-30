from django.contrib.auth import get_user_model
from django.db.models import Q
from itertools import chain

from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cinema_critic_server.common.helper_functions.get_content_model import get_model
from cinema_critic_server.common.models import Genre
from cinema_critic_server.common.serializers import GenreSerializer
from cinema_critic_server.content.models import Movie, Series
from cinema_critic_server.content.serializers.serializers_content import ContentSerializer
from cinema_critic_server.content.serializers.serializers_movies import MovieReadSerializer
from cinema_critic_server.content.serializers.serializers_series import SeriesReadSerializer

UserModel = get_user_model()


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


class BookmarkListView(generics.ListAPIView):
    serializer_class = ContentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = get_object_or_404(UserModel, id=user_id)
        profile = user.profile
        bookmarks_movies = list(profile.bookmarks_movies.all())
        bookmarks_series = list(profile.bookmarks_series.all())
        return bookmarks_movies + bookmarks_series


class BookmarkItemView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, content_type, content_id):
        content_model = get_model(content_type)
        content = get_object_or_404(content_model, id=content_id)

        profile = request.user.profile
        profile.add_bookmark(content)  # add_bookmarks / remove_bookmark are methods of 'Profile'
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)

    @staticmethod
    def delete(request, content_type, content_id):
        content_model = get_model(content_type)
        content = get_object_or_404(content_model, id=content_id)

        profile = request.user.profile
        profile.remove_bookmark(content)
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)
