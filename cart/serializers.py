from rest_framework import serializers
from .models import Cart, CartItem
from products.serializers import ProductSerializer  # Import the ProductSerializer

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()  # Use ProductSerializer for the product field

    class Meta:
        model = CartItem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'
