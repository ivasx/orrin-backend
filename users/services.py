from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification

def notify_user(recipient, actor, notification_type, target_object=None, text=""):
    if recipient == actor:
        return

    notification = Notification.objects.create(
        recipient=recipient,
        actor=actor,
        notification_type=notification_type,
        content_object=target_object,
        text=text  # Може бути пустим
    )

    channel_layer = get_channel_layer()
    payload = {
        "id": notification.id,
        "notification_type": notification.notification_type,
        "is_read": False,
        "created_at": notification.created_at.isoformat(),
        "actor": {
            "username": actor.username,
            "avatar": actor.avatar.url if actor.avatar else None
        }
    }

    async_to_sync(channel_layer.group_send)(
        f"user_{recipient.id}_notifications",
        {
            "type": "send_notification",
            "message": payload
        }
    )