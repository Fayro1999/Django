# serializers.py
from rest_framework import serializers
from .models import DeliveryDetail, DeliveryTime, PaymentMethod

class DeliveryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryDetail
        fields = '__all__'

class DeliveryTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryTime
        fields = '__all__'

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'
