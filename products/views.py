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

    
class ProductUpdateView(generics.UpdateAPIView):
    permission_classes = [AllowAny]  # Adjust permissions as needed
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'  # Use 'id' or another unique field in the model

# Delete product view
class ProductDeleteView(generics.DestroyAPIView):
    permission_classes = [AllowAny]  # Adjust permissions as needed
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'  # Use 'id' or another unique field in the model



    def get_queryset(self):
        vendor_id = self.request.query_params.get('vendor_id')
        if vendor_id:
            return Product.objects.filter(vendor_id=vendor_id)
        return Product.objects.all()
