from django.db import models
from django.conf import settings

class StoreUserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='store_user_profiles',
        blank=True,
        help_text='The groups this user belongs to.',
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




class StoreDetails(models.Model):
    store_user_profile = models.OneToOneField(StoreUserProfile, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=255)
    store_address = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    cac_image = models.ImageField(upload_to='cac_images/')

    def __str__(self):
        return self.store_name
