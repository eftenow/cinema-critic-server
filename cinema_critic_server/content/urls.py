from django.urls import path

from cinema_critic_server.content.views import MovieListCreateView, MovieDetailsEditDeleteView, SeriesListCreateView, \
    SeriesDetailsEditDeleteView, ContentListView, SearchView

urlpatterns = [
    path('all/', ContentListView.as_view(), name='content_list'),
    # responsible for returning both movies and series at once

    path('movies/', MovieListCreateView.as_view(), name='movies_list_create'),
    # responsible for returning movies and creating new movie

    path('movies/<int:pk>/', MovieDetailsEditDeleteView.as_view(), name='movie_detail'),
    # responsible for movie details/edit/delete

    path('series/', SeriesListCreateView.as_view(), name='series_list_create'),
    # responsible for returning series and creating new series

    path('series/<int:pk>/', SeriesDetailsEditDeleteView.as_view(), name='series_detail'),
    # responsible for series details/edit/delete

    path('search/', SearchView.as_view(), name='search_content'),
    # responsible for returning searched content based on given queryset

]
