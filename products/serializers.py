from rest_framework import serializers
from .models import Product
from stores.models import StoreUserProfile  # Import StoreUserProfile

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['vendor']  # Prevent users from manually setting vendor

    def create(self, validated_data):
        request = self.context.get('request')  # Get request from context
        if request and hasattr(request, "user") and request.user.is_authenticated:
            store_profile = StoreUserProfile.objects.filter(user=request.user).first()  # Get Store Profile
            if store_profile and hasattr(store_profile, "store_details"):  # Check if StoreDetails exists
                validated_data['vendor'] = store_profile.store_details  # ✅ Correctly assign StoreDetails
            else:
                raise serializers.ValidationError("You must have a store to create a product.")
        return super().create(validated_data)

