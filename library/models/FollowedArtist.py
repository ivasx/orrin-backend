from django.conf import settings
from django.db import models


class FollowedArtist(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followed_artists',
    )
    artist = models.ForeignKey(
        'orrin.Artist',
        on_delete=models.CASCADE,
        related_name='followers',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'artist')
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=['user', 'artist']),
        ]

    def __str__(self):
        return f'{self.user} follows {self.artist}'
