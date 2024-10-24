from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer
from rest_framework.permissions import  AllowAny #IsAuthenticated

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
        vendor_id = self.request.query_params.get('vendor_id')
        if vendor_id:
            return Product.objects.filter(vendor_id=vendor_id)
        return Product.objects.all()
