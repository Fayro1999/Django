from rest_framework import serializers
from .models import DispatchRider

class DispatchRiderSerializer(serializers.ModelSerializer):
    rider_id = serializers.CharField(read_only=True)
    
    class Meta:
        model = DispatchRider
        fields = ['user', 'phone', 'company', 'location', 'rider_id']
        extra_kwargs = {
            'user': {'required': True}  # Ensure user info is provided
        }

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = get_user_model().objects.create_user(**user_data)  # Ensure user is created correctly
        
        dispatch_rider = DispatchRider.objects.create(
            user=user,
            phone=validated_data['phone'],
            company=validated_data['company'],
            location=validated_data['location'],
        )
        return dispatch_rider
