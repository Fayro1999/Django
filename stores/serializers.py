from rest_framework import serializers
from rest_framework import serializers
from rest_framework import serializers
from .models import StoreUserProfile
from authent.models import CustomUser
from authent.serializers import UserSerializer  # Assuming this serializer handles the user fields

class StoreSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Serialize the related user object

    class Meta:
        model = StoreUserProfile
        fields = ['user', 'phone', 'groups', 'user_permissions']  # Include the user-related fields through the user serializer

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        
        # Use create_user to properly handle password and user creation
        user = CustomUser.objects.create_user(
            email=user_data['email'],
            username=user_data['email'],  # Set email as username
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            phone=user_data['phone'],
            password=user_data['password']  # Handle password correctly
        )
        
        # Create the store profile with the newly created user
        store_user_profile = StoreUserProfile.objects.create(user=user, **validated_data)
        return store_user_profile

