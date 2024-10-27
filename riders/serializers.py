from rest_framework import serializers
from .models import DispatchRider
from django.contrib.auth import get_user_model

User = get_user_model()

class DispatchRiderSerializer(serializers.ModelSerializer):
    rider_id = serializers.CharField(read_only=True)  # Add rider_id as read-only
    email = serializers.EmailField(write_only=True)  # Set email as write-only field for input

    class Meta:
        model = DispatchRider
        fields = ['email', 'phone', 'company', 'location', 'rider_id']  # Removed password from here
        extra_kwargs = {
            'phone': {'required': True},
            'company': {'required': True},
            'location': {'required': True},
            'rider_id': {'read_only': True},  # Ensure rider_id is read-only
        }

    def create(self, validated_data):
        email = validated_data.pop('email')  # Extract the email
        password = self.context['request'].data.get('password')  # Get password from context

        # Create the user instance with email as the username
        user = User(email=email)  # Create a User instance with email
        user.set_password(password)  # Set the password
        user.save()  # Save the user instance

        # Create the DispatchRider instance linked to the user
        dispatch_rider = DispatchRider.objects.create(user=user, **validated_data)
        return dispatch_rider

    def get_email(self, obj):
        return obj.user.email if obj.user else None  # Access email from user profile
