from rest_framework import serializers

from users.models import Notification


class ActorSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    avatar = serializers.SerializerMethodField()

    def get_avatar(self, obj):
        request = self.context.get("request")
        if obj.avatar and hasattr(obj.avatar, "url"):
            return request.build_absolute_uri(obj.avatar.url) if request else obj.avatar.url
        return None


class NotificationSerializer(serializers.ModelSerializer):
    actor = ActorSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = (
            "id",
            "notification_type",
            "actor",
            "text",
            "is_read",
            "created_at",
        )
        read_only_fields = fields
