from rest_framework import serializers
from .models import StoreUserProfile
from authent.serializers import UserSerializer  # Assuming this serializer handles the user fields

class StoreSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Serialize the related user object

    class Meta:
        model = StoreUserProfile
        fields = ['user', 'groups', 'user_permissions']  # Include user-related fields through the user serializer

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = CustomUser.objects.create(**user_data)
        store_user_profile = StoreUserProfile.objects.create(user=user, **validated_data)
        return store_user_profile

