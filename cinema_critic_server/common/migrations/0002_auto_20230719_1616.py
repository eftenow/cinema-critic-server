# Generated by Django 4.2.3 on 2023-07-19 16:16

from django.db import migrations


def create_genres(apps, schema_editor):
    Genre = apps.get_model('common', 'Genre')
    CHOICES = (
        ('action', 'Action'),
        ('animation', 'Animation'),
        ('adventure', 'Adventure'),
        ('comedy', 'Comedy'),
        ('crime', 'Crime'),
        ('drama', 'Drama'),
        ('sci-fi', 'Sci-Fi'),
        ('fantasy', 'Fantasy'),
        ('horror', 'Horror'),
        ('mystery', 'Mystery'),
        ('romance', 'Romance'),
    )
    for choice in CHOICES:
        Genre.objects.create(name=choice[0])


class Migration(migrations.Migration):
    dependencies = [
        ('common', '0001_initial'),  # replace with your actual previous migration
    ]

    operations = [
        migrations.RunPython(create_genres),
    ]
