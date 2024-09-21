# notifications/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_authenticated:
            # Subscribe the user to their notifications channel
            await self.channel_layer.group_add(
                f'notifications_{self.user.id}',
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        # Unsubscribe from notifications channel
        await self.channel_layer.group_discard(
            f'notifications_{self.user.id}',
            self.channel_name
        )

    async def receive(self, text_data):
        pass  # Not required for notifications

    # Called by the channel layer when a new notification is sent
    async def send_notification(self, event):
        await self.send(text_data=json.dumps(event['notification']))
