from rest_framework import serializers
from rest_framework import serializers
from rest_framework import serializers
from .models import StoreUserProfile
from authent.models import CustomUser
from authent.serializers import UserSerializer  # Assuming this serializer handles the user fields
from .models import StoreDetails
from products.models import Product
from products.serializers import ProductSerializer


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



class StoreProfileCombinedSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Use existing UserSerializer for user details
    store_details = serializers.SerializerMethodField()  # Add store details dynamically

    class Meta:
        model = StoreUserProfile
        fields = ['user', 'groups', 'user_permissions', 'store_details', 'products']

    def get_store_details(self, obj):
        """
        Dynamically fetch store details for the StoreUserProfile instance.
        """
        try:
            store_details = StoreDetails.objects.get(store_user_profile=obj)
            return StoreDetailsSerializer(store_details).data  # Use existing StoreDetailsSerializer
        except StoreDetails.DoesNotExist:
            return None


    def get_products(self, obj):
        # Fetch products associated with this store
        products = Product.objects.filter(store_user_profile=obj)
        return ProductSerializer(products, many=True).data