from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
import random
import string

class DispatchRiderManager(BaseUserManager):
    def create_user(self, email, phone, company, location, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        user = self.model(
            email=self.normalize_email(email),
            phone=phone,
            company=company,
            location=location,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, company, location, password=None):
        user = self.create_user(
            email,
            phone=phone,
            company=company,
            location=location,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class DispatchRider(AbstractBaseUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    rider_id = models.CharField(max_length=12, unique=True, blank=True)  # Rider ID field
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = DispatchRiderManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'company', 'location']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    # Custom save method to generate rider_id
    def save(self, *args, **kwargs):
        if not self.rider_id:
            # Generate rider ID: "EL" + 3 random digits + first 3 letters of location
            random_digits = ''.join(random.choices(string.digits, k=3))
            location_prefix = self.location[:3].upper()
            self.rider_id = f"EL{random_digits}{location_prefix}"
        super().save(*args, **kwargs)
