# Generated by Django 5.0.6 on 2024-10-27 08:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('riders', '0002_alter_dispatchrider_email_alter_dispatchrider_phone'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dispatchrider',
            name='email',
        ),
        migrations.RemoveField(
            model_name='dispatchrider',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='dispatchrider',
            name='is_admin',
        ),
        migrations.RemoveField(
            model_name='dispatchrider',
            name='last_login',
        ),
        migrations.RemoveField(
            model_name='dispatchrider',
            name='password',
        ),
        migrations.AddField(
            model_name='dispatchrider',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dispatch_rider_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]