class FilterSortMixin:
    def get_filtered_sorted_queryset(self, queryset):

        genres = self.request.query_params.get('genres')
        if genres:
            genres = genres.split(',')
            for genre in genres:
                queryset = queryset.filter(genres__name=genre)

        sort = self.request.query_params.get('sort')
        print('before', queryset)
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
