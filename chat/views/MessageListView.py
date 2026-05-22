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
        if not text:
            return Response(
                {"detail": "text is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        message = Message.objects.create(chat=chat, sender=request.user, text=text)
        chat.save()

        serializer = MessageSerializer(message, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)