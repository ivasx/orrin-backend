from django.contrib.auth import get_user_model
from rest_framework import serializers

from chat.models import Message

User = get_user_model()


class LastMessageSerializer(serializers.ModelSerializer):
    senderId = serializers.IntegerField(source="sender_id", read_only=True)
    timestamp = serializers.DateTimeField(source="created_at", read_only=True)
    isRead = serializers.BooleanField(source="is_read", read_only=True)

    class Meta:
        model = Message
        fields = ("id", "senderId", "text", "timestamp", "isRead")
