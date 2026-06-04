from django.conf import settings
from django.db import models


class Note(models.Model):
    """
    A user-written annotation attached to a track and/or an artist.

    - `note_type='public'`  — visible to other users.
    - `note_type='private'` — visible only to the author.

    Optional fields:
    - `timecode`     — second offset within the track (floating-point).
    - `lyric_line`   — reference to a specific synced lyric line.
    - `track`        — the track this note is about (may be null for artist-only notes).
    - `artist`       — the artist this note is about (may be null for track-only notes).
    """

    NOTE_TYPE_CHOICES = (
        ('public', 'Public'),
        ('private', 'Private'),
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notes',
        verbose_name='Author',
    )
    track = models.ForeignKey(
        'orrin.Track',
        on_delete=models.CASCADE,
        related_name='notes',
        null=True,
        blank=True,
        verbose_name='Track',
    )
    artist = models.ForeignKey(
        'orrin.Artist',
        on_delete=models.CASCADE,
        related_name='notes',
        null=True,
        blank=True,
        verbose_name='Artist',
    )
    lyric_line = models.ForeignKey(
        'orrin.LyricLine',
        on_delete=models.SET_NULL,
        related_name='notes',
        null=True,
        blank=True,
        verbose_name='Lyric line reference',
    )
    text = models.TextField(verbose_name='Note text')
    note_type = models.CharField(
        max_length=10,
        choices=NOTE_TYPE_CHOICES,
        default='public',
        verbose_name='Visibility',
    )
    timecode = models.FloatField(
        null=True,
        blank=True,
        verbose_name='Timecode (seconds)',
        help_text='Offset in seconds within the track.',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=['track', 'note_type']),
            models.Index(fields=['artist', 'note_type']),
            models.Index(fields=['author', 'note_type']),
        ]
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(track__isnull=False) |
                    models.Q(artist__isnull=False)
                ),
                name='note_must_have_track_or_artist',
            ),
        ]

    def __str__(self):
        target = self.track or self.artist
        return f'{self.author} on {target}: {self.text[:60]}'
