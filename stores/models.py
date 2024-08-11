from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)  # Add phone field
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='store_user_set',  # Add a unique related_name
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='store_user_set',  # Add a unique related_name
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )
