# Generated by Django 5.1.6 on 2025-02-11 23:20

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
