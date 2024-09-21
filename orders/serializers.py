# orders/serializers.py
from rest_framework import serializers
from .models import Order
from products.serializers import ProductSerializer
from delivery.models import DeliveryDetail
from stores.models import StoreDetails
from products.models import Product

class DeliveryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryDetail
        fields = ['reciever_name', 'reciever_mobile', 'reciver_address']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'image']  # Adjust based on your product model

class StoreDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreDetails
        fields = ['store_name', 'store_address']

class OrderSerializer(serializers.ModelSerializer):
    delivery = DeliveryDetailSerializer()  # Include delivery details
    products = ProductSerializer(many=True)  # Include product details
    store = StoreDetailsSerializer()  # Include store details

    class Meta:
        model = Order
        fields = ['id', 'store', 'products', 'quantity', 'amount', 'status', 'date', 'delivery']



class OrderAuthenticationSerializer(serializers.Serializer):
    order_id = serializers.CharField()
    customer_name = serializers.CharField()  # We'll match the customer's full name or part of it

    def validate(self, data):
        order_id = data.get('order_id')
        customer_name = data.get('customer_name')

        # We'll match the order ID and the customer name
        try:
            order = Order.objects.get(order_id=order_id)
            full_name = f"{order.user.first_name} {order.user.last_name}"
            if customer_name.lower() not in full_name.lower():
                raise serializers.ValidationError("Customer name does not match the provided order.")
        except Order.DoesNotExist:
            raise serializers.ValidationError("Order with the provided ID does not exist.")
        
        return data

    def authenticate_order(self):
        validated_data = self.validated_data
        order = Order.objects.get(order_id=validated_data['order_id'])
        return order


