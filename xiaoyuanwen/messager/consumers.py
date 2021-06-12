import json

from channels.generic.websocket import AsyncWebsocketConsumer


class MessagesConsumer(AsyncWebsocketConsumer):
    """处理私信应用中的Websocket请求"""
    async def connect(self):
        """加入聊天组"""
        if self.scope['user'].is_anonymous:
            await self.close()
        else:
            await self.channel_layer.group_add(self.scope['user'].username, self.channel_name)
            await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        """接收私信"""
        await self.send(text_data=json.dumps(text_data))

    async def disconnect(self, code):
        """离开聊天组"""
        await self.channel_layer.group_discard(self.scope['user'].username, self.channel_name)
