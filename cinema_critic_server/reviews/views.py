from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from .models import Review
from .serializers import ReviewSerializer


class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_random_text(self):
        if self.request.user.is_authenticated:
            return "You are authenticated!"
        else:
            return "You are not authenticated!"

    def list(self, request, *args, **kwargs):
        random_text = self.get_random_text()
        print(random_text)  # Or do whatever you want with the random_text
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']  # Retrieve user_id from the URL
        return Review.objects.filter(user__id=user_id)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)
        if request.method == 'PUT' or request.method == 'DELETE':
            if request.user != obj.user:
                raise PermissionDenied('You can not edit this review')
