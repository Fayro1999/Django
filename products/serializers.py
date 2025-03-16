from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['vendor']  # Prevent users from manually setting vendor

    def create(self, validated_data):
        request = self.context.get('request')  # Get request from context
        if request and hasattr(request, "user") and request.user.is_authenticated:
            if hasattr(request.user, "store_details"):
                validated_data['vendor'] = request.user.store_details  # Assign store
            else:
                raise serializers.ValidationError("You must have a store to create a product.")
        return super().create(validated_data)
