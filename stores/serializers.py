from rest_framework import serializers
from .models import StoreUserProfile
from authent.serializers import UserSerializer  # Assuming this serializer handles the user fields
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class StoreSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = StoreUserProfile
        fields = ['user', 'groups', 'user_permissions']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = CustomUser.objects.create(
            email=user_data['email'],
            username=user_data['email'],  # Set email as the username
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            phone=user_data['phone'],
            is_active=False  # The user will be inactive until email verification
        )
        store_user_profile = StoreUserProfile.objects.create(user=user, **validated_data)
        return store_user_profile
