# Generated by Django 4.2.3 on 2023-07-22 13:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_movie_slug_series_slug_alter_movie_director_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=2, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)]),
        ),
        migrations.AlterField(
            model_name='movie',
            name='visits',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='series',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=2, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)]),
        ),
        migrations.AlterField(
            model_name='series',
            name='visits',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]