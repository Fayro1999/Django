# notifications/serializers.py
from rest_framework import serializers
from .models import Notification
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'read', 'timestamp', 'notification_type']  # Add notification_type
