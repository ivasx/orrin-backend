from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import Notification

_NOTIFICATION_TEXT_DEFAULTS = {
    'new_track': 'released a new track',
    'new_post': 'published a new post',
    'like_post': 'liked your post',
    'like_comment': 'liked your comment',
    'follow': 'started following you',
    'reply': 'replied to your comment',
}


def notify_user(recipient, actor, notification_type, target_object=None, text=''):
    if recipient == actor:
        return

    resolved_text = text or _NOTIFICATION_TEXT_DEFAULTS.get(notification_type, '')

    notification = Notification.objects.create(
        recipient=recipient,
        actor=actor,
        notification_type=notification_type,
        content_object=target_object,
        text=resolved_text,
    )

    channel_layer = get_channel_layer()

    avatar_url = actor.avatar.url if actor.avatar else None

    payload = {
        'id': notification.id,
        'notification_type': notification.notification_type,
        'text': notification.text,
        'is_read': False,
        'created_at': notification.created_at.isoformat(),
        'actor': {
            'id': actor.id,
            'username': actor.username,
            'avatar': avatar_url,
        },
    }

    async_to_sync(channel_layer.group_send)(
        f'user_{recipient.id}_notifications',
        {
            'type': 'send_notification',
            'message': payload,
        },
    )