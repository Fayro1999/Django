from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count
from .models import Product
from stores.models import StoreUserProfile
from .serializers import ProductSerializer
from rest_framework.views import APIView
from rest_framework import status


# Creating product view
class ProductCreateView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        """Pass request context to serializer"""
        return {'request': self.request}

# List product view with sorting and store filtering
class ProductListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer

    def get_queryset(self):
        store_id = self.request.query_params.get('store_id')
        sort_by = self.request.query_params.get('sort', 'newest')

        queryset = Product.objects.all()

        if store_id:
            queryset = queryset.filter(store_id=store_id)

        if sort_by == 'newest':
            return queryset.order_by('-created_at')[:10]
        elif sort_by == 'trending':
            return queryset.order_by('-views')[:10]
        elif sort_by == 'most_searched':
            return queryset.order_by('-search_count')[:10]
        elif sort_by == 'best_sellers':
            return queryset.order_by('-sales')[:10]

        return queryset

# Product Detail View with View Count Increment
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        """Override retrieve method to increment view count"""
        instance = self.get_object()
        instance.increment_views()  # Increase view count
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

# Top Selling Stores View
class TopSellingStoresView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer

    def get_queryset(self):
        """Retrieve stores sorted by total sales count"""
        return StoreUserProfile.objects.annotate(
            total_sales=Count('product__sales')
        ).order_by('-total_sales')[:10]

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


class StoreProductsView(APIView):
    def get(self, request, store_id):
        products = Product.objects.filter(vendor_id=store_id)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)