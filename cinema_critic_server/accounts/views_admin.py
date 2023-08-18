from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.db.models import Case, When, Value, IntegerField


def get_users(request):
    if not request.user.is_staff:
        return JsonResponse({'error': 'Permission denied'}, status=403)

    UserModel = get_user_model()

    # custom ordering for user roles so that they appear sorted in the front-end
    ordering = Case(
        When(groups__name="Administrator", then=Value(1)),
        When(groups__name="Moderator", then=Value(2)),
        When(groups__name="Regular User", then=Value(3)),
        default=Value(4),
        output_field=IntegerField()
    )

    users = UserModel.objects.annotate(role_order=ordering).order_by('role_order', 'username')

    users_data = []
    for user in users:
        role = user.groups.all().first()
        role_name = role.name if role else "No Role"

        user_data = {
            'id': user.id,
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
