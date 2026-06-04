from django.conf import settings
from django.db import models


class NoteLike(models.Model):
    """Records a like by a user on a public note."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='note_likes',
    )
    note = models.ForeignKey(
        'notes.Note',
        on_delete=models.CASCADE,
        related_name='likes',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'note')
        indexes = [
            models.Index(fields=['note']),
        ]

    def __str__(self):
        return f'{self.user} liked note {self.note_id}'
