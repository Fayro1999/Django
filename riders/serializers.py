from rest_framework import serializers
from .models import DispatchRider
from django.contrib.auth import get_user_model

User = get_user_model()

class DispatchRiderSerializer(serializers.ModelSerializer):
    rider_id = serializers.CharField(read_only=True)  # Add rider_id as read-only

    class Meta:
        model = DispatchRider
        fields = ['email', 'phone', 'company', 'location', 'password', 'rider_id']
        extra_kwargs = {
            'password': {'write_only': True},  # Ensure password is write-only
        }

    def create(self, validated_data):
        email = validated_data.pop('email')  # Extract the email
        password = validated_data.pop('password')  # Extract the password

        # Create the user instance with email as the username
        user = User(email=email)  # Create a User instance with email
        user.set_password(password)  # Set the password
        user.save()  # Save the user instance

        # Create the DispatchRider instance linked to the user
        dispatch_rider = DispatchRider.objects.create(user=user, **validated_data)
        return dispatch_rider
