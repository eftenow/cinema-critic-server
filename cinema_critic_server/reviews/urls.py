from django.urls import path
from .views import ReviewListCreateView, UserReviewListView, ReviewDetailView, MovieReviewListView, SeriesReviewListView

urlpatterns = [
    path('', ReviewListCreateView.as_view(), name='review_list_create'),
    path('user/<int:user_id>/', UserReviewListView.as_view(), name='user_review_list'),
    path('<int:pk>/', ReviewDetailView.as_view(), name='review_detail'),
    path('movie/<int:id>/', MovieReviewListView.as_view(), name='movie-reviews'),
    path('series/<int:id>/', SeriesReviewListView.as_view(), name='series-reviews'),
]
