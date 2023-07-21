from rest_framework import serializers

from cinema_critic_server.content.models import Movie, Series
from cinema_critic_server.content.movies_serializers import MovieReadSerializer
from cinema_critic_server.content.serializers.serializers_series import SeriesReadSerializer


class ContentSerializer(serializers.Serializer):
    def to_representation(self, instance):
        if isinstance(instance, Movie):
            return MovieReadSerializer(instance).data
        if isinstance(instance, Series):
            return SeriesReadSerializer(instance).data