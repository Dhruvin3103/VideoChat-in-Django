# Generated by Django 4.2.4 on 2023-08-20 06:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('videochat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lobby',
            name='lobby_users',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
