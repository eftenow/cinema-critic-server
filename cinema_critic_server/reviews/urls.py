from django.urls import path
from .views import ReviewListCreateView, UserReviewListView, ReviewDetailsEditDeleteView

urlpatterns = [
    path('', ReviewListCreateView.as_view(), name='review_list_create'),
    # responsible for returning all reviews at once per 'GET' and to create new review on 'POST'
    path('user/<int:user_id>/', UserReviewListView.as_view(), name='user_review_list'),
    # responsible for returning specified user's reviews
    path('<int:pk>/', ReviewDetailsEditDeleteView.as_view(), name='review_detail'),
    # responsible for returning review details upon 'GET', editing it upon 'PUT' or deleting it upon 'DELETE'

]
