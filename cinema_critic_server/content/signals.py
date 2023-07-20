from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from .models import Movie, Series


@receiver(post_save, sender=Movie)
def update_movie_slug(sender, instance, created, **kwargs):
    if created:
        instance.slug = slugify(f'{instance.name}-{instance.id}')
        instance.save()


@receiver(post_save, sender=Series)
def update_series_slug(sender, instance, created, **kwargs):
    if created:
        instance.slug = slugify(f'{instance.name}-{instance.id}')
        instance.save()
