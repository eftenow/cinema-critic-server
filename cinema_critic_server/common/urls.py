from django.urls import path
from .views import ContentSearchListView, GenresListView, BookmarkListView, BookmarkItemView

urlpatterns = [
    path('search/', ContentSearchListView.as_view(), name='content_search'),
    path('genres/', GenresListView.as_view(), name='all_genres_list_'),
    path('bookmarks/<int:user_id>/', BookmarkListView.as_view(), name='bookmark-list'),
    path('bookmarks/<str:content_type>/<int:content_id>/', BookmarkItemView.as_view(), name='bookmark-item'),
]
