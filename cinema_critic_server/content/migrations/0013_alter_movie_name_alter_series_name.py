# Generated by Django 4.2.3 on 2023-08-18 16:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0012_movie_creator_series_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='name',
            field=models.CharField(max_length=60, validators=[django.core.validators.MinLengthValidator(2)]),
        ),
        migrations.AlterField(
            model_name='series',
            name='name',
            field=models.CharField(max_length=60, validators=[django.core.validators.MinLengthValidator(2)]),
        ),
    ]