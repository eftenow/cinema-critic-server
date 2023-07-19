from rest_framework import serializers

from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'review_title', 'user', 'content', 'rating', 'content_type', 'object_id', 'content_object']
