from rest_framework import serializers
from .models import DispatchRider
from django.contrib.auth import get_user_model

User = get_user_model()

class DispatchRiderSerializer(serializers.ModelSerializer):
    rider_id = serializers.CharField(read_only=True)  # Add rider_id as read-only
    email = serializers.EmailField()  # Ensure email is included for user creation
    password = serializers.CharField(write_only=True)  # Ensure password is write-only

    class Meta:
        model = DispatchRider
        fields = ['email', 'phone', 'company', 'location', 'password', 'rider_id']
        extra_kwargs = {
            'password': {'write_only': True},  # Ensure password is write-only
        }

    def create(self, validated_data):
        # Create the CustomUser first
        user = User.objects.create_user(
            email=validated_data['email'],
            phone=validated_data['phone'],  # Assuming your CustomUser has a phone field
            password=validated_data['password']
        )
        
        # Now create the DispatchRider profile
        dispatch_rider = DispatchRider.objects.create(
            user=user,  # Link to the CustomUser
            company=validated_data['company'],
            location=validated_data['location'],
        )
        
        return dispatch_rider
