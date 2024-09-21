# store_locations/urls.py
from django.urls import path
from .views import StoreLocationListView

urlpatterns = [
    path('store-locations/', StoreLocationListView.as_view(), name='store-locations'),
]
