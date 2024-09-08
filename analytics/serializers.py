from rest_framework import serializers
from .models import StoreVisitor, StoreOrder, StoreRevenue, StoreCart, VisitorPurchase

class StoreVisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreVisitor
        fields = '__all__'

class StoreOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreOrder
        fields = '__all__'

class StoreRevenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreRevenue
        fields = '__all__'

class StoreCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreCart
        fields = '__all__'

class VisitorPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitorPurchase
        fields = '__all__'
