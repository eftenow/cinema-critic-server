from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


UserModel = get_user_model()


class Review(models.Model):
    review_title = models.CharField(max_length=30)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    rating = models.IntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
