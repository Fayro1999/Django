# Generated by Django 5.2 on 2025-05-06 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('groceries', 'Groceries'), ('appliances', 'Appliances'), ('household_cleaning', 'Household Cleaning'), ('electronics', 'Electronics'), ('other', 'Other Category')], default='other', max_length=50),
        ),
    ]
