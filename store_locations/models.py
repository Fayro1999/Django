# store_locations/models.py
from django.db import models
from geopy.geocoders import Nominatim
from django.db.models.signals import post_save
from django.dispatch import receiver
from stores.models import StoreDetails

class StoreLocation(models.Model):
    store = models.OneToOneField(StoreDetails, on_delete=models.CASCADE)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.store.store_name} - {self.latitude}, {self.longitude}"

# Function to automatically get lat/long when a store location is created
@receiver(post_save, sender=StoreDetails)
def create_store_location(sender, instance, created, **kwargs):
    if created:
        geolocator = Nominatim(user_agent="Eazzi")
        location = geolocator.geocode(instance.store_address)
        if location:
            StoreLocation.objects.create(
                store=instance, latitude=location.latitude, longitude=location.longitude
            )
