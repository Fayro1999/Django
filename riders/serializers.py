from rest_framework import serializers
from .models import DispatchRider
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model


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
            phone=validated_data['phone'],
            company=validated_data['company'],
            location=validated_data['location'],
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise serializers.ValidationError('Both email and password are required')

        user = authenticate(request=self.context.get('request'), email=email, password=password)
        if user is None:
            raise serializers.ValidationError('Invalid email or password')

        return {'user': user}
