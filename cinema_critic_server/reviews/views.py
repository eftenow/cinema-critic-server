from django.contrib.contenttypes.models import ContentType
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from .models import Review
from .serializers import ReviewSerializer


class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        content_type = ContentType.objects.get(model=self.request.data['content_type'])
        serializer.save(user=self.request.user, content_type=content_type)
        instance = serializer.instance
        instance.content_object.update_rating()


class UserReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Review.objects.filter(user__id=user_id)


class ReviewDetailsEditDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)
        if request.method == 'PUT' or request.method == 'DELETE':
            user_is_administrator = request.user.groups.filter(name='Administrator').exists()
            if not user_is_administrator and request.user != obj.user:
                raise PermissionDenied('You can not edit this review')

    def perform_update(self, serializer):
        content_type = ContentType.objects.get(model=self.request.data['content_type'])
        serializer.save()
        instance = serializer.instance
        instance.content_object.update_rating()

    def perform_destroy(self, instance):
        content_object = instance.content_object
        instance.delete()
        content_object.update_rating()


class MovieReviewsListView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        movie_id = self.kwargs['id']
        content_type = ContentType.objects.get(model='movie')
        return Review.objects.filter(content_type=content_type, object_id=movie_id)


class SeriesReviewsListView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        series_id = self.kwargs['id']
        content_type = ContentType.objects.get(model='series')
        return Review.objects.filter(content_type=content_type, object_id=series_id)
