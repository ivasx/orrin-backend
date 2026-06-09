from rest_framework import serializers

from users.models import Notification


class NotificationActorSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.SerializerMethodField()
    username = serializers.CharField()
    avatarUrl = serializers.SerializerMethodField()

    def get_name(self, obj):
        full = f'{obj.first_name} {obj.last_name}'.strip()
        return full or obj.username

    def get_avatarUrl(self, obj):
        request = self.context.get('request')
        if obj.avatar and hasattr(obj.avatar, 'url'):
            return request.build_absolute_uri(obj.avatar.url) if request else obj.avatar.url
        return None


class NotificationEntitySerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    coverUrl = serializers.SerializerMethodField()

    def get_id(self, obj):
        return obj.object_id

    def get_title(self, obj):
        entity = obj.content_object
        if entity is None:
            return None
        return getattr(entity, 'title', None) or getattr(entity, 'name', None)

    def get_coverUrl(self, obj):
        entity = obj.content_object
        if entity is None:
            return None
        request = self.context.get('request')
        for field in ('cover', 'image', 'cover_photo', 'avatar'):
            cover = getattr(entity, field, None)
            if cover and hasattr(cover, 'url'):
                return request.build_absolute_uri(cover.url) if request else cover.url
        return None


class NotificationSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='notification_type', read_only=True)
    isRead = serializers.BooleanField(source='is_read', read_only=True)
    timestamp = serializers.DateTimeField(source='created_at', read_only=True)
    actor = serializers.SerializerMethodField()
    entity = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = (
            'id',
            'type',
            'isRead',
            'timestamp',
            'actor',
            'entity',
        )

    def get_actor(self, obj):
        return NotificationActorSerializer(obj.actor, context=self.context).data

    def get_entity(self, obj):
        if obj.content_object is None:
            return None
        return NotificationEntitySerializer(obj, context=self.context).data
