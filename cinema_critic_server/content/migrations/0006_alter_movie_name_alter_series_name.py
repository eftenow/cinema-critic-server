# Generated by Django 4.2.3 on 2023-07-26 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0005_movie_description_series_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='name',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='series',
            name='name',
            field=models.CharField(max_length=40),
        ),
    ]