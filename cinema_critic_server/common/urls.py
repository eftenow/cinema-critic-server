from django.urls import path
from .views import ContentSearchListView

urlpatterns = [
    path('search/', ContentSearchListView.as_view(), name='content-search'),
]
