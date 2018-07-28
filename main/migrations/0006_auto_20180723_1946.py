# Generated by Django 2.0.2 on 2018-07-23 19:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0002_logentry_remove_auto_add'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0005_auto_20180723_1400'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='ratings',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_ptr',
        ),
        migrations.AddField(
            model_name='movie',
            name='rated_by',
            field=models.ManyToManyField(through='main.RatingMovie', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='party',
            name='party_memberships',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ratingmovie',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]