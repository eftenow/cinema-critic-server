from django.urls import path
from .views import ReviewListCreateView, UserReviewListView, ReviewDetailView

urlpatterns = [
    path('', ReviewListCreateView.as_view(), name='review_list_create'),
    path('user/<int:user_id>/', UserReviewListView.as_view(), name='user_review_list'),
    path('<int:pk>/', ReviewDetailView.as_view(), name='review_detail'),
]