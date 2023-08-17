from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.http import JsonResponse

UserModel = get_user_model()


def get_users(request):
    if not request.user.is_staff:
        return JsonResponse({'error': 'Permission denied'}, status=403)

    UserModel = get_user_model()

    users_data = []
    users = UserModel.objects.all()
    for user in users:
        role = user.groups.all().first()
        role_name = role.name if role else "No Role"
        user_data = {
            'username': user.username,
            'email': user.email,
            'role': role_name
        }
        users_data.append(user_data)
    """
        by specifying safe=False, we guarantee that we want to return a list
        this is used when returning lists/sets/tuples, and not dictionaries, which
        django typically expects 
        """
    return JsonResponse(users_data, safe=False)