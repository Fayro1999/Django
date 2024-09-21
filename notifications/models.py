# notifications/models.py
from django.db import models
from django.conf import settings
class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('order', 'Order Update'),
        ('promotion', 'Promotion'),
        ('message', 'Message'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    message = models.TextField()
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)  # New field

