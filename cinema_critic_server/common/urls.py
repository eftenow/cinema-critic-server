from django.urls import path
from .views import ContentSearchListView, GenresListView

urlpatterns = [
    path('search/', ContentSearchListView.as_view(), name='content_search'),
    path('genres/', GenresListView.as_view(), name='all_genres_list_')
]
