# Generated by Django 4.2.3 on 2023-07-26 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0004_alter_movie_rating_alter_series_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='series',
            name='description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
