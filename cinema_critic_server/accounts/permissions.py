from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from cinema_critic_server.content.models import Movie, Series

admin_group, created = Group.objects.get_or_create(name='Administrator')

for perm in Permission.objects.all():
    admin_group.permissions.add(perm)


moderator_group, created = Group.objects.get_or_create(name='Moderator')
content_types = [ContentType.objects.get_for_model(Movie), ContentType.objects.get_for_model(Series)]

for content_type in content_types:
    for operation in ["add", "change", "delete"]:
        permission = Permission.objects.get(content_type=content_type, codename=f"{operation}_{content_type.model}")
        moderator_group.permissions.add(permission)
