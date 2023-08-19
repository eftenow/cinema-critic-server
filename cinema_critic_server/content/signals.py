from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver
from django.utils.text import slugify
from .models import Movie, Series
from ..reviews.models import Review


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



@receiver(post_delete, sender=Movie)
def delete_associated_reviews_for_movie(sender, instance, **kwargs):
    delete_associated_reviews(instance)


@receiver(post_delete, sender=Series)
def delete_associated_reviews_for_series(sender, instance, **kwargs):
    delete_associated_reviews(instance)


def delete_associated_reviews(instance):
    content_type = ContentType.objects.get_for_model(instance)

    Review.objects.filter(content_type=content_type, object_id=instance.id).delete()
