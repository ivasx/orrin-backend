from django.db import models


class Lyrics(models.Model):
    """
    Stores lyrics for a track.

    Two modes:
    - 'static'  — plain text, no timestamps.  `plain_text` is populated,
                  LyricLine rows are not created.
    - 'synced'  — karaoke-style.  `plain_text` is empty/ignored,
                  LyricLine rows carry per-line timestamps.
    """

    LYRICS_TYPE_CHOICES = (
        ('static', 'Static'),
        ('synced', 'Synced'),
    )

    track = models.OneToOneField(
        'Track',
        on_delete=models.CASCADE,
        related_name='lyrics',
        verbose_name='Track',
    )
    lyrics_type = models.CharField(
        max_length=10,
        choices=LYRICS_TYPE_CHOICES,
        default='static',
        verbose_name='Lyrics type',
    )
    # Used only when lyrics_type == 'static'
    plain_text = models.TextField(
        blank=True,
        default='',
        verbose_name='Plain text lyrics',
    )

    class Meta:
        verbose_name = 'Lyrics'
        verbose_name_plural = 'Lyrics'

    def __str__(self):
        return f'Lyrics for {self.track} ({self.lyrics_type})'


class LyricLine(models.Model):
    """
    A single timestamped line for synced lyrics.
    Order is defined by `time_seconds` ascending.
    """

    lyrics = models.ForeignKey(
        Lyrics,
        on_delete=models.CASCADE,
        related_name='lines',
        verbose_name='Lyrics',
    )
    time_seconds = models.FloatField(
        verbose_name='Start time (seconds)',
        help_text='Timestamp in seconds when this line starts.',
    )
    text = models.CharField(max_length=500, verbose_name='Line text')

    class Meta:
        ordering = ('time_seconds',)
        verbose_name = 'Lyric line'
        verbose_name_plural = 'Lyric lines'

    def __str__(self):
        return f'[{self.time_seconds:.2f}s] {self.text[:60]}'
