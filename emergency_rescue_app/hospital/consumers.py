import json
from channels.generic.websocket import AsyncWebsocketConsumer

class EmergencyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add(
            'emergency_alerts',
            self.channel_name
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'emergency_alerts',
            self.channel_name
        )

    async def send_emergency_alert(self, event):
        await self.send(text_data=json.dumps({
            'type': 'emergency_alert',
            'data': event['data'],
        }))