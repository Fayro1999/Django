from django.db import models
from django.conf import settings
import random
import string

class DispatchRider(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)  # Link to CustomUser
    phone = models.CharField(max_length=20)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    rider_id = models.CharField(max_length=12, unique=True, blank=True)  # Rider ID field
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)






    USERNAME_FIELD = 'email'  # Use email as the username field
    REQUIRED_FIELDS = [] 




    

    def __str__(self):
        return self.user.email  # Return email for better readability

    # Custom save method to generate rider_id
    def save(self, *args, **kwargs):
        if not self.rider_id:
            # Generate rider ID: "EL" + 3 random digits + first 3 letters of location
            random_digits = ''.join(random.choices(string.digits, k=3))
            location_prefix = self.location[:3].upper()
            self.rider_id = f"EL{random_digits}{location_prefix}"
        super().save(*args, **kwargs)
