from django.contrib.auth import get_user_model
from rest_framework import serializers

from chat.models import Chat
from chat.serializers.LastMessageSerializer import LastMessageSerializer
from chat.serializers.ParticipantSerializer import ParticipantSerializer

User = get_user_model()


class ChatSerializer(serializers.ModelSerializer):
    participant = serializers.SerializerMethodField()
    lastMessage = serializers.SerializerMethodField()
    unreadCount = serializers.SerializerMethodField()
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)

    class Meta:
        model = Chat
        fields = ("id", "participant", "lastMessage", "unreadCount", "updatedAt")

    def get_participant(self, obj):
        request = self.context.get("request")
        other = obj.get_other_participant(request.user)
        if not other:
            return None
        return ParticipantSerializer(other, context=self.context).data

    def get_lastMessage(self, obj):
        last = obj.messages.order_by("-created_at").first()
        if not last:
            return None
        return LastMessageSerializer(last).data

    def get_unreadCount(self, obj):
        request = self.context.get("request")
        return obj.messages.filter(is_read=False).exclude(sender=request.user).count()
