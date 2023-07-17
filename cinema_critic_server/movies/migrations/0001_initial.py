# Generated by Django 4.2.3 on 2023-07-17 12:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('year', models.IntegerField(validators=[django.core.validators.MinValueValidator(1900)])),
                ('rating', models.IntegerField(blank=True, null=True)),
                ('director', models.CharField(max_length=20)),
                ('stars', models.CharField(max_length=50)),
                ('visits', models.IntegerField(blank=True, null=True)),
                ('genres', models.CharField(max_length=30)),
                ('trailer', models.URLField()),
                ('image', models.URLField()),
                ('length', models.CharField(max_length=20)),
            ],
        ),
    ]
