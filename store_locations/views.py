# store_locations/views.py
from rest_framework import generics
from .models import StoreLocation
from .serializers import StoreLocationSerializer

class StoreLocationListView(generics.ListAPIView):
    queryset = StoreLocation.objects.all()
    serializer_class = StoreLocationSerializer
