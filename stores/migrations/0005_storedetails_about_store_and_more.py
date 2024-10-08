# Generated by Django 5.0.6 on 2024-09-16 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0004_storedetails'),
    ]

    operations = [
        migrations.AddField(
            model_name='storedetails',
            name='about_store',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='storedetails',
            name='background_image',
            field=models.ImageField(blank=True, null=True, upload_to='store_backgrounds/'),
        ),
        migrations.AddField(
            model_name='storedetails',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='store_profiles/'),
        ),
        migrations.AddField(
            model_name='storedetails',
            name='working_hours',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
