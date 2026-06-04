from django.conf import settings
from django.db import models


class SavedAlbum(models.Model):
    """Records an album saved/bookmarked by a user."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='saved_albums',
    )
    album = models.ForeignKey(
        'orrin.Album',
        on_delete=models.CASCADE,
        related_name='saved_by',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'album')
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=['user', 'created_at']),
        ]

    def __str__(self):
        return f'{self.user} saved {self.album}'
