from django.db import models
from django.conf import settings


class StoreUserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    verification_code = models.CharField(max_length=6, null=True, blank=True)
    verification_code_expiration = models.DateTimeField(null=True, blank=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='store_user_profiles',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='store_user_profile',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='store_user_permissions_profiles',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='store_user_profile',
    )

    def __str__(self):
        return f'{self.user.email} - Store Profile'

