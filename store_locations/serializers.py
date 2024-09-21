# store_locations/serializers.py
from rest_framework import serializers
from .models import StoreLocation

class StoreLocationSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source='store.store_name')

    class Meta:
        model = StoreLocation
        fields = ['store_name', 'latitude', 'longitude']
