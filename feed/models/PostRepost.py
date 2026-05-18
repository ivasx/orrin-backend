from django.conf import settings
from django.db import models


class PostRepost(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reposts',
    )
    post = models.ForeignKey(
        'feed.Post',
        on_delete=models.CASCADE,
        related_name='reposts',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
        indexes = [
            models.Index(fields=['post']),
        ]
