# Generated by Django 5.1.6 on 2025-02-11 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('received', 'Received'), ('pending', 'Pending'), ('completed', 'Completed')], max_length=10)),
                ('order_id', models.CharField(blank=True, max_length=20, unique=True)),
            ],
        ),
    ]
