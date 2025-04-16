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


        # Unsave a product
class UnsaveProductView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = SavedProduct.objects.all()

    def delete(self, request, *args, **kwargs):
        product_id = kwargs.get("product_id")
        saved_product = get_object_or_404(SavedProduct, user=request.user, product_id=product_id)
        saved_product.delete()
        return Response({"message": "Product unsaved"}, status=204)


        # Check if a product is saved
class CheckSavedProductView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, product_id):
        is_saved = SavedProduct.objects.filter(user=request.user, product_id=product_id).exists()
        return Response({"is_saved": is_saved})


# Saving stores
class SavedStoreListCreateView(generics.ListCreateAPIView):
    serializer_class = SavedStoreSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SavedStore.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


        # Unsave a store
class UnsaveStoreView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = SavedStore.objects.all()

    def delete(self, request, *args, **kwargs):
        store_id = kwargs.get("store_id")
        saved_store = get_object_or_404(SavedStore, user=request.user, store_id=store_id)
        saved_store.delete()
        return Response({"message": "Store unsaved"}, status=204)


# Check if a store is saved
class CheckSavedStoreView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, store_id):
        is_saved = SavedStore.objects.filter(user=request.user, store_id=store_id).exists()
        return Response({"is_saved": is_saved})

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
