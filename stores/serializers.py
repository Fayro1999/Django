from rest_framework import serializers
from rest_framework import serializers
from rest_framework import serializers
from .models import StoreUserProfile
from authent.models import CustomUser
from authent.serializers import UserSerializer  # Assuming this serializer handles the user fields
from .models import StoreDetails

class StoreSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Serialize the related user object

    class Meta:
        model = StoreUserProfile
        fields = ['user', 'groups', 'user_permissions']

    def create(self, validated_data):
        user_data = validated_data.pop('user')  # Remove 'user' from validated_data

        # Create the user object first
        user = CustomUser.objects.create_user(
            email=user_data['email'],
            username=user_data['email'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            phone=user_data['phone'],
            password=user_data['password']
        )
        print("User created:", user.email)

        # Handle groups and permissions
        groups = validated_data.pop('groups', [])
        user_permissions = validated_data.pop('user_permissions', [])

        # Create the StoreUserProfile without 'user' keyword argument
        store_user_profile = StoreUserProfile.objects.create(user=user)
        print("StoreUserProfile created:", store_user_profile)

        # Set additional fields manually
        store_user_profile.groups.set(groups)
        store_user_profile.user_permissions.set(user_permissions)

        return store_user_profile



class StoreDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreDetails
        fields = '__all__'
