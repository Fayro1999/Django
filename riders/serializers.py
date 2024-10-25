from rest_framework import serializers
from .models import DispatchRider


class DispatchRiderSerializer(serializers.ModelSerializer):
    rider_id = serializers.CharField(read_only=True)  # Add rider_id as read-only

    class Meta:
        model = DispatchRider
        fields = ['email', 'phone', 'company', 'location', 'password', 'rider_id']  # Include rider_id
        extra_kwargs = {
            'password': {'write_only': True},  # Ensure password is write-only
        }

    def create(self, validated_data):
        user = DispatchRider.objects.create_user(
            email=validated_data['email'],
            username=validated_data['email'],
            phone=validated_data['phone'],
            company=validated_data['company'],
            location=validated_data['location'],
            password=validated_data['password']
        )
        return user



