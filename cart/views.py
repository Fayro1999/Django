from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import AllowAny #IsAuthenticated
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from products.models import Product  # Import the Product model

class CartDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = CartSerializer

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

class AddToCartView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        if not product_id:
            return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity = quantity
        cart_item.save()

        return Response({"message": "Product added to cart"}, status=status.HTTP_201_CREATED)

class RemoveFromCartView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')

        if not product_id:
            return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        cart = Cart.objects.get(user=request.user)
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.delete()
            return Response({"message": "Product removed from cart"}, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response({"error": "Product not in cart"}, status=status.HTTP_404_NOT_FOUND)


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    @action(detail=True, methods=['patch'])
    def update_quantity(self, request, pk=None):
        cart_item = self.get_object()
        quantity = request.data.get('quantity')
        if quantity is not None and int(quantity) > 0:
            cart_item.quantity = int(quantity)
            cart_item.save()
            return Response(CartItemSerializer(cart_item).data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
