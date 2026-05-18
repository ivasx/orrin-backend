from django.conf import settings
from django.db import models


class PostComment(models.Model):
    post = models.ForeignKey(
        'feed.Post',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='post_comments',
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=['post', 'created_at']),
        ]

    def __str__(self):
        return f'{self.author} on post {self.post_id}: {self.text[:40]}'
