from django.urls import path
from .views import ReviewListCreateView, UserReviewListView, ReviewDetailsEditDeleteView, MovieReviewsListView, \
    SeriesReviewsListView

urlpatterns = [
    path('', ReviewListCreateView.as_view(), name='review_list_create'),
    # responsible for returning all reviews for all movies/series at once per 'GET'
    # and to create new review on 'POST'
    path('user/<int:user_id>/', UserReviewListView.as_view(), name='user_review_list'),
    # responsible for returning specified user's reviews
    path('<int:pk>/', ReviewDetailsEditDeleteView.as_view(), name='specific_review_detail'),
    # responsible for returning review details upon 'GET', editing it upon 'PUT' or deleting it upon 'DELETE'
    path('movie/<int:id>/', MovieReviewsListView.as_view(), name='specific_movie_reviews'),
    # responsible for returning all reviews for specific movie object
    path('series/<int:id>/', SeriesReviewsListView.as_view(), name='specific_series_reviews'),
    # responsible for returning all reviews for specific series object
]
