from channels.generic.websocket import AsyncWebsocketConsumer
import json

class SegmentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
       

        await self.accept()

       

        await self.channel_layer.group_add(
            "segments",
            self.channel_name
        )

       

   
    async def segment_update(self, event):
       

        await self.send(text_data=json.dumps(event["data"]))