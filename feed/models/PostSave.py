from django.conf import settings
from django.db import models


class PostSave(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='saved_posts',
    )
    post = models.ForeignKey(
        'feed.Post',
        on_delete=models.CASCADE,
        related_name='saves',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
        indexes = [
            models.Index(fields=['user', 'created_at']),
        ]
