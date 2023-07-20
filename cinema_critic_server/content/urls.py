from django.urls import path

from cinema_critic_server.content.views import MovieListCreateView, SeriesListCreateView

urlpatterns = [
    path('movies/', MovieListCreateView.as_view(), name='display movies'),
    path('movies/create', MovieListCreateView.as_view(), name='create movie'),
    path('movies/edit', MovieListCreateView.as_view(), name='edit movie'),
    path('movies/delete', MovieListCreateView.as_view(), name='delete movie'),
    path('series/', SeriesListCreateView.as_view(), name='display series'),
]
