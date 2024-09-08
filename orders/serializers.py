from rest_framework import serializers
from orders.models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_id', 'store', 'user', 'products', 'quantity', 'date', 'amount', 'status']

