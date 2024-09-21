from rest_framework import serializers
from .models import StoreVisitor, StoreOrder, StoreRevenue, StoreCart, VisitorPurchase, WebsiteVisitor, WebsiteOrder, WebsiteRevenue, WebsiteCart, WebsitePurchase

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



# website analytics serializers

class WebsiteVisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebsiteVisitor
        fields = '__all__'

class WebsiteOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebsiteOrder
        fields = '__all__'

class WebsiteRevenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebsiteRevenue
        fields = '__all__'

class WebsiteCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebsiteCart
        fields = '__all__'

class WebsitePurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebsitePurchase
        fields = '__all__'
