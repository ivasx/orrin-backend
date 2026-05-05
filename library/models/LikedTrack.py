from django.conf import settings
from django.db import models


class LikedTrack(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='liked_tracks',
    )
    track = models.ForeignKey(
        'orrin.Track',
        on_delete=models.CASCADE,
        related_name='liked_by',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'track')
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=['user', 'track']),
        ]

    def __str__(self):
        return f'{self.user} liked {self.track}'
