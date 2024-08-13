from rest_framework import serializers
from rest_framework import serializers
from .models import StoreUserProfile
from authent.models import CustomUser
from authent.serializers import UserSerializer  # Assuming this serializer handles the user fields

class StoreSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Serialize the related user object

    class Meta:
        model = StoreUserProfile
        fields = ['user', 'groups', 'user_permissions']  # Include user-related fields through the user serializer

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = CustomUser.objects.create(
            email=user_data['email'],
            username=user_data['email'],  # Set email as username
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            phone=user_data['phone'],
        )
        user.set_password(user_data['password'])
        user.save()

        store_user_profile = StoreUserProfile.objects.create(user=user, **validated_data)
        return store_user_profile
