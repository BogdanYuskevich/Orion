import json
from channels.generic.websocket import AsyncWebsocketConsumer

class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Додаємо підключення до групи "dashboard"
        await self.channel_layer.group_add("dashboard", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # При відключенні видаляємо з групи
        await self.channel_layer.group_discard("dashboard", self.channel_name)

    # Метод, який викликається, коли надходить повідомлення з групи
    async def dashboard_notification(self, event):
        notification = event['notification']
        await self.send(text_data=json.dumps({
            'notification': notification
        }))
