import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from chat.models import Chat, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.room_group = f"chat_{self.chat_id}"

        if self.user.is_anonymous:
            await self.close()
            return

        has_access = await self._user_in_chat()
        if not has_access:
            await self.close()
            return

        await self.channel_layer.group_add(self.room_group, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "room_group"):
            await self.channel_layer.group_discard(self.room_group, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            return

        event_type = data.get("type")

        if event_type == "typing_start":
            await self.channel_layer.group_send(
                self.room_group,
                {
                    "type": "chat.typing_start",
                    "senderId": self.user.id,
                    "chatId": self.chat_id,
                },
            )

        elif event_type == "typing_stop":
            await self.channel_layer.group_send(
                self.room_group,
                {
                    "type": "chat.typing_stop",
                    "senderId": self.user.id,
                    "chatId": self.chat_id,
                },
            )

        elif event_type == "send_message":
            text = (data.get("text") or "").strip()
            if not text:
                return

            message = await self._create_message(text)
            if message is None:
                return

            await self.channel_layer.group_send(
                self.room_group,
                {
                    "type": "chat.receive_message",
                    "message": {
                        "id": message.id,
                        "chatId": message.chat_id,
                        "senderId": message.sender_id,
                        "text": message.text,
                        "timestamp": message.created_at.isoformat(),
                        "isRead": message.is_read,
                    },
                },
            )

    async def chat_receive_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "receive_message",
            **event["message"],
        }))

    async def chat_typing_start(self, event):
        if event["senderId"] == self.user.id:
            return
        await self.send(text_data=json.dumps({
            "type": "typing_start",
            "senderId": event["senderId"],
            "chatId": event["chatId"],
        }))

    async def chat_typing_stop(self, event):
        if event["senderId"] == self.user.id:
            return
        await self.send(text_data=json.dumps({
            "type": "typing_stop",
            "senderId": event["senderId"],
            "chatId": event["chatId"],
        }))

    @sync_to_async
    def _user_in_chat(self):
        return Chat.objects.filter(pk=self.chat_id, participants=self.user).exists()

    @sync_to_async
    def _create_message(self, text):
        try:
            chat = Chat.objects.get(pk=self.chat_id, participants=self.user)
        except Chat.DoesNotExist:
            return None
        message = Message.objects.create(chat=chat, sender=self.user, text=text)
        chat.save()
        return message
