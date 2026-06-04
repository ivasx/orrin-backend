from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        # track-related
        ('new_track', 'New Track'),
        ('like_track', 'Like Track'),
        # post-related
        ('new_post', 'New Post'),
        ('like_post', 'Like Post'),
        ('like_comment', 'Like Comment'),
        ('reply', 'Comment Reply'),
        # social
        ('follow', 'New Follower'),
        # library
        ('playlist_add', 'Added to Playlist'),
        # artist
        ('new_release', 'New Release'),
    )

    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
    )
    actor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='actions_caused',
    )
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)

    # Generic relation — can point at any model (Track, Post, Album, Playlist …)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
        ]

    def __str__(self):
        return (
            f'{self.actor.username} → {self.recipient.username}: '
            f'{self.notification_type}'
        )
