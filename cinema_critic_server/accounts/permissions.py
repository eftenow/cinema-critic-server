from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from cinema_critic_server.accounts.models import Profile
from cinema_critic_server.content.models import Movie, Series
from cinema_critic_server.reviews.models import Review

admin_group, created = Group.objects.get_or_create(name='Administrator')

for perm in Permission.objects.all():
    admin_group.permissions.add(perm)

moderator_group, created = Group.objects.get_or_create(name='Moderator')
content_types = [ContentType.objects.get_for_model(Movie), ContentType.objects.get_for_model(Series)]

for content_type in content_types:
    for operation in ["add", "change", "delete"]:
        permission = Permission.objects.get(content_type=content_type, codename=f"{operation}_{content_type.model}")
        moderator_group.permissions.add(permission)


def setup_regular_user_group():
    """
    here i get the 'add_review permission and the 'change_profile' permission and then i assign them to the
    'Regular' group
    """
    regular_user_group, created = Group.objects.get_or_create(name='Regular User')

    content_type = ContentType.objects.get_for_model(Review)
    add_review_permission = Permission.objects.get(content_type=content_type, codename='add_review')

    content_type = ContentType.objects.get_for_model(Profile)
    change_profile_permission = Permission.objects.get(content_type=content_type, codename='change_profile')

    regular_user_group.permissions.add(add_review_permission, change_profile_permission)
