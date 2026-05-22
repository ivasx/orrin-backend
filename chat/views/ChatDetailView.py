from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from chat.models import Chat
from chat.serializers import ChatSerializer


class ChatDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=['Chat'])
    def get(self, request, pk):
        chat = (
            Chat.objects
            .filter(pk=pk, participants=request.user)
            .prefetch_related("participants")
            .first()
        )
        if not chat:
            return Response(
                {"detail": "Chat not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = ChatSerializer(chat, context={"request": request})
        return Response(serializer.data)