from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import SavedProduct, SavedStore, ProductReview, StoreReview
from .serializers import SavedProductSerializer, SavedStoreSerializer, ProductReviewSerializer, StoreReviewSerializer

# Saving products
class SavedProductListCreateView(generics.ListCreateAPIView):
    serializer_class = SavedProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SavedProduct.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Saving stores
class SavedStoreListCreateView(generics.ListCreateAPIView):
    serializer_class = SavedStoreSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SavedStore.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Reviews for products
class ProductReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ProductReview.objects.filter(product_id=self.kwargs['product_id'])

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Reviews for stores
class StoreReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = StoreReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return StoreReview.objects.filter(store_id=self.kwargs['store_id'])

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
