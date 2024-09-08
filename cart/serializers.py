# cart/serializers.py
from rest_framework import serializers
from products.serializers import ProductSerializer
from .models import CartItem, Cart

class CartItemSerializer(serializers.ModelSerializer):
    amount = serializers.ReadOnlyField()  # Computed field for total amount (price * quantity)
    product = ProductSerializer()  # Include product details
    
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'amount']



class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, source='cartitem_set')  # Use the reverse relation to include cart items
    total_amount = serializers.SerializerMethodField()
    user = serializers.ReadOnlyField(source='user.username')  # Include the username of the user

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_amount']

    def get_total_amount(self, obj):
        return sum(item.amount for item in obj.cartitem_set.all())
