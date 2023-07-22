from rest_framework.pagination import PageNumberPagination


class MoviesSeriesPaginator(PageNumberPagination):
    page_size = 12

