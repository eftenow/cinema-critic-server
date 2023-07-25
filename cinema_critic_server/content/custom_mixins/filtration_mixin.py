class FilterSortMixin:
    """
    This mixin filters and sorts querysets by using their built-in sorting
    and filtering functionalities. It is built as a mixin, because it is
    used in multiple places - Movies view, Series view and Content view.
    """
    def get_filtered_sorted_queryset(self, queryset):

        genres = self.request.query_params.get('genres')
        if genres:
            genres = genres.split(',')
            for genre in genres:
                queryset = queryset.filter(genres__name=genre)

        sort = self.request.query_params.get('sort')

        if sort:
            if sort.lower() == 'newest':
                queryset = queryset.order_by('-created_at')
            elif sort.lower() == 'oldest':
                queryset = queryset.order_by('created_at')
            elif sort.lower() == 'highest_rating':
                queryset = queryset.order_by('-rating')
            elif sort.lower() == 'lowest_rating':
                queryset = queryset.order_by('rating')

        return queryset.distinct()


class ContentSortMixin:
    """
    This mixin is specifically for the Content View, because I had to use another
    sorting approach, unlike the one that is in the FilterSortMixin. This is because
    for the 'Content' we need fields that are contained in 2 separate Models - Movies
    and Series, so in order to combine them and sort them together, I had to turn them
    to a list. And unlike querysets, lists do not have built-in sorting functionality,
    so I had to do it manually using lambda function in this case.
    """
    def sort_all_content(self, content_list, sort):
        if sort:
            if sort.lower() == 'newest':
                content_list.sort(key=lambda x: x.created_at, reverse=True)
            elif sort.lower() == 'oldest':
                content_list.sort(key=lambda x: x.created_at)
            elif sort.lower() == 'highest_rating':
                content_list.sort(key=lambda x: x.rating, reverse=True)
            elif sort.lower() == 'lowest_rating':
                content_list.sort(key=lambda x: x.rating)

        return content_list
