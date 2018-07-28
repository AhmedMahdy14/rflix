# Generated by Django 2.0.2 on 2018-07-24 14:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20180724_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ratingmovie',
            name='p_rating',
            field=models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)]),
        ),
    ]