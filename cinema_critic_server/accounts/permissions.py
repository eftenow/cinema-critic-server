import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cinema_critic_server.settings")
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from cinema_critic_server.accounts.models import Profile
from cinema_critic_server.content.models import Movie, Series
from cinema_critic_server.reviews.models import Review

"""
run this file alone in order to apply the admin groups
"""


def setup_administrator_group():
    """
    Setup the Administrator group and assign all permissions.
    """
    admin_group, created = Group.objects.get_or_create(name='Administrator')
    for perm in Permission.objects.all():
        admin_group.permissions.add(perm)


def setup_moderator_group():
    """
    Setup the Moderator group and assign permissions related to Movie and Series models.
    """
    moderator_group, created = Group.objects.get_or_create(name='Moderator')
    content_types = [ContentType.objects.get_for_model(Movie), ContentType.objects.get_for_model(Series)]

    for content_type in content_types:
        for operation in ["add", "change", "delete"]:
            permission = Permission.objects.get(content_type=content_type, codename=f"{operation}_{content_type.model}")
            moderator_group.permissions.add(permission)


def setup_regular_user_group():
    """
    Setup the Regular User group and assign permissions related to Review and Profile models.
    """
    regular_user_group, created = Group.objects.get_or_create(name='Regular User')

    content_type = ContentType.objects.get_for_model(Review)
    add_review_permission = Permission.objects.get(content_type=content_type, codename='add_review')

    content_type = ContentType.objects.get_for_model(Profile)
    change_profile_permission = Permission.objects.get(content_type=content_type, codename='change_profile')

    regular_user_group.permissions.add(add_review_permission, change_profile_permission)


# Call the functions to setup groups and permissions
setup_administrator_group()
setup_moderator_group()
setup_regular_user_group()
