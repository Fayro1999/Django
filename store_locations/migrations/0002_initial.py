# Generated by Django 5.2 on 2025-05-05 17:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store_locations', '0001_initial'),
        ('stores', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='storelocation',
            name='store',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='stores.storedetails'),
        ),
    ]
