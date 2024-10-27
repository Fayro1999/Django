from django.db import models
import random
import string
from django.conf import settings  # For referencing AUTH_USER_MODEL

class DispatchRider(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # Link to CustomUser
        on_delete=models.CASCADE,
        related_name="dispatch_rider_profile",
        null=True
    )
    phone = models.CharField(max_length=20, null=True, blank=True, default="0000000000")
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    rider_id = models.CharField(max_length=12, unique=True, blank=True)  # Rider ID field


    USERNAME_FIELD = 'email'  # Set email as the username field
    REQUIRED_FIELDS = []  # Add other required fields if any

    def __str__(self):
        return f"Dispatch Rider: {self.user.email}"

    # Custom save method to generate rider_id
    def save(self, *args, **kwargs):
        if not self.rider_id:
            # Generate rider ID: "EL" + 3 random digits + first 3 letters of location
            random_digits = ''.join(random.choices(string.digits, k=3))
            location_prefix = self.location[:3].upper()
            self.rider_id = f"EL{random_digits}{location_prefix}"
        super().save(*args, **kwargs)
