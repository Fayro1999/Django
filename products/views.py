from rest_framework import generics
from .models import Product 
from stores.models import StoreUserProfile,StoreDetails
from .serializers import ProductSerializer
from rest_framework.permissions import AllowAny
from django.db.models import Count
from rest_framework.response import Response

# Creating product view
class ProductCreateView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# List product view
class ProductListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        store_id = self.request.query_params.get('store_id')
        if store_id:
            return Product.objects.filter(store_id=store_id)
        return Product.objects.all()

#Product View
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        """Override retrieve method to increment view count"""
        instance = self.get_object()  # Get the product
        instance.increment_views()  # Increase the views count
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

# Newest Products View
class NewestProductsView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all().order_by('-created_at')[:10]

# Top Selling Stores View
class TopSellingStoresView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer

    def get_queryset(self):
        return StoreUserProfile.objects.annotate(
            num_sales=Count('order')
        ).order_by('-num_sales')[:10]

# Trending Products View
class TrendingProductsView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all().order_by('-views')[:10]

# Best Sellers in Accessories View
class BestSellersInAccessoriesView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(category='Accessories').order_by('-sales')[:10]

# Most Searched Products View
class MostSearchedProductsView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all().order_by('-search_count')[:10]

# Update product view
class ProductUpdateView(generics.UpdateAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

# Delete product view
class ProductDeleteView(generics.DestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

    def get_queryset(self):
        vendor_id = self.request.query_params.get('vendor_id')
        if vendor_id:
            return Product.objects.filter(vendor_id=vendor_id)
        return Product.objects.all()
