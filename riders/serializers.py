from rest_framework import serializers
from .models import DispatchRider
from django.contrib.auth import authenticate


class DispatchRiderSerializer(serializers.ModelSerializer):
    class Meta:
        model = DispatchRider
        fields = ['email', 'phone', 'company', 'location', 'password']

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

        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError('Invalid email or password')

        return {'user': user}

