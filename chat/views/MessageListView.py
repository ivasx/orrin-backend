from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from chat.models import Chat, Message
from chat.serializers import MessageSerializer


class MessageListView(APIView):
    permission_classes = [IsAuthenticated]

    def _get_chat(self, request, pk):
        return (
            Chat.objects
            .filter(pk=pk, participants=request.user)
            .first()
        )

    @extend_schema(tags=['Chat'])
    def get(self, request, pk):
        chat = self._get_chat(request, pk)
        if not chat:
            return Response(
                {"detail": "Chat not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        Message.objects.filter(
            chat=chat,
            is_read=False,
        ).exclude(sender=request.user).update(is_read=True)

        messages = chat.messages.select_related("sender").order_by("created_at")
        serializer = MessageSerializer(messages, many=True, context={"request": request})
        return Response(serializer.data)

    @extend_schema(tags=['Chat'])
    def post(self, request, pk):
        chat = self._get_chat(request, pk)
        if not chat:
            return Response(
                {"detail": "Chat not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        text = request.data.get("text", "").strip()
        track_id = request.data.get("track_id") or request.data.get("trackId")

        if not text and not track_id:
            return Response(
                {"detail": "text or track_id is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        message = Message.objects.create(
            chat=chat,
            sender=request.user,
            text=text,
            track_id=track_id,
        )
        chat.save()

        serializer = MessageSerializer(message, context={"request": request})
        message_data = serializer.data

        # Broadcast to WebSocket group so all participants receive it in real time
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"chat_{pk}",
            {
                "type": "chat.receive_message",
                "message": {
                    "id": message_data["id"],
                    "chatId": message_data["chatId"],
                    "senderId": message_data["senderId"],
                    "text": message_data["text"],
                    "trackId": message_data["trackId"],
                    "timestamp": message_data["timestamp"],
                    "isRead": message_data["isRead"],
                },
            },
        )

        return Response(message_data, status=status.HTTP_201_CREATED)
