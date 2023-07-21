from django.urls import path

from cinema_critic_server.content.views import MovieListCreateView, MovieDetailView, SeriesListCreateView, \
    SeriesDetailView, ContentListView

urlpatterns = [
    path('', ContentListView.as_view(), name='content_list'),
    # responsible for returning both movies and series at once

    path('movies/', MovieListCreateView.as_view(), name='movies_list_create'),
    # responsible for returning movies and creating new movie

    path('movies/<int:pk>/', MovieDetailView.as_view(), name='movie_detail'),
    # responsible for movie details/edit/delete

    path('series/', SeriesListCreateView.as_view(), name='series_list_create'),
    # responsible for returning series and creating new series

    path('series/<int:pk>/', SeriesDetailView.as_view(), name='series_detail'),
    # responsible for series details/edit/delete

]
