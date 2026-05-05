from django.conf import settings
from django.db import models


HISTORY_LIMIT = 500


class ListeningHistory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='listening_history',
    )
    track = models.ForeignKey(
        'orrin.Track',
        on_delete=models.CASCADE,
        related_name='history_entries',
    )
    played_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-played_at',)
        indexes = [
            models.Index(fields=['user', 'played_at']),
        ]

    def __str__(self):
        return f'{self.user} played {self.track} at {self.played_at}'
