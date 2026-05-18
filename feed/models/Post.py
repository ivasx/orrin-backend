from django.conf import settings
from django.db import models


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    text = models.TextField()
    track = models.ForeignKey(
        'orrin.Track',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=['author', 'created_at']),
        ]

    def __str__(self):
        return f'{self.author} — {self.text[:50]}'
