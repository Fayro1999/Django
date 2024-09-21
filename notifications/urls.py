from django.urls import path
from .views import NotificationListView, MarkNotificationReadView

urlpatterns = [
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/read/<int:notification_id>/', MarkNotificationReadView.as_view(), name='notification-read'),
]
