# Generated by Django 4.2.3 on 2023-08-19 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_alter_review_review_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='review_title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
