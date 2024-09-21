# notifications/views.py
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer



class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get all notifications for the logged-in user
        notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

class MarkNotificationReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, notification_id):
        try:
            notification = Notification.objects.get(id=notification_id, user=request.user)
            notification.read = True
            notification.save()
            return Response({"message": "Notification marked as read."})
        except Notification.DoesNotExist:
            return Response({"error": "Notification not found."}, status=404)


def send_real_time_notification(user, notification):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'notifications_{user.id}',
        {
            'type': 'send_notification',
            'notification': {
                'title': notification.title,
                'message': notification.message,
                'timestamp': str(notification.timestamp),
            }
        }
    )