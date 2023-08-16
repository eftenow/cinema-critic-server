from django.contrib.auth.models import User
from django.http import JsonResponse


def get_users(request):
    if not request.user.is_staff:
        return JsonResponse({'error': 'Permission denied'}, status=403)

    users = User.objects.all().values('username', 'email')
    """
    by specifying safe=False, we guarantee that we want to return a list
    this is used when returning lists/sets/tuples, and not dictionaries, which
    django typically expects 
    """
    return JsonResponse(list(users), safe=False)
