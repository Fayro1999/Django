from rest_framework import serializers
from .models import SavedProduct, SavedStore, ProductReview, StoreReview

class SavedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedProduct
        fields = '__all__'

class SavedStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedStore
        fields = '__all__'

class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = '__all__'

class StoreReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreReview
        fields = '__all__'
