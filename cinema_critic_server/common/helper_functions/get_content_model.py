from django.apps import apps


def get_model(content_type):
    """
    the built-in "apps.get_model()" takes 2 arguments, first one - the name of the application where the model
    is located and the second one - the specific model
    """
    if content_type == 'movie':
        return apps.get_model('content', 'Movie')
    elif content_type == 'series':
        return apps.get_model('content', 'Series')
    else:
        return None
