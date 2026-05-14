from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from chat.models import Chat
from chat.serializers import ChatSerializer

User = get_user_model()


class ChatListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        chats = (
            Chat.objects
            .filter(participants=request.user)
            .prefetch_related("participants", "messages")
            .order_by("-updated_at")
        )
        serializer = ChatSerializer(chats, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        recipient_username = request.data.get("recipient_username", "").strip()
        if not recipient_username:
            return Response(
                {"detail": "recipient_username is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        recipient = User.objects.filter(username=recipient_username).first()
        if not recipient:
            return Response(
                {"detail": "User not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if recipient == request.user:
            return Response(
                {"detail": "You cannot start a chat with yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        existing = (
            Chat.objects
            .filter(participants=request.user)
            .filter(participants=recipient)
            .first()
        )
        if existing:
            serializer = ChatSerializer(existing, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        chat = Chat.objects.create()
        chat.participants.add(request.user, recipient)

        serializer = ChatSerializer(chat, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
