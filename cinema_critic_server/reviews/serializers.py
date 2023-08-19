from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    content_type = serializers.SlugRelatedField(
        queryset=ContentType.objects.all(),
        slug_field='model'
    )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('user', )

    def validate_content_type(self, value):
        if value.model not in ['movie', 'series']:
            raise serializers.ValidationError("Invalid content type. Expected 'movie' or 'series'.")
        return value

    def create(self, validated_data):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            validated_data['user'] = user
        return super().create(validated_data)
