import io

import mutagen
from django.core.files.storage import default_storage
from django.db import models
from django.urls import reverse

from .SluggedModel import SluggedModel


class Track(SluggedModel):
    """
    Represents a music track with metadata and media files.

    `plays_count` is a denormalised counter incremented via a signal every time
    a ListeningHistory entry is created.  It allows cheap ordering/display
    without an expensive COUNT aggregate on hot paths.
    """

    slug_source_fields = ['title', 'artist']

    title = models.CharField(max_length=255, verbose_name='Title')
    artist = models.ForeignKey(
        'Artist',
        on_delete=models.CASCADE,
        verbose_name='Artist',
        related_name='tracks',
    )
    cover = models.ImageField(
        upload_to='images/covers/',
        blank=True,
        null=True,
        verbose_name='Cover image',
    )
    audio = models.FileField(
        upload_to='audio/',
        blank=True,
        null=True,
        verbose_name='Audio file',
    )
    duration = models.PositiveIntegerField(
        help_text='Track duration in seconds.',
        blank=True,
        default=0,
        null=True,
        verbose_name='Duration',
    )
    plays_count = models.PositiveBigIntegerField(
        default=0,
        verbose_name='Play count',
        help_text='Denormalised counter incremented on each listen.',
        db_index=True,
    )

    def __str__(self):
        return f'{self.title} — {self.artist}'

    def duration_formatted(self):
        if not self.duration:
            return '0:00'
        minutes, seconds = divmod(self.duration, 60)
        return f'{minutes}:{seconds:02d}'

    def get_absolute_url(self):
        return reverse('track-detail-api', kwargs={'slug': self.slug})

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _extract_duration(self):
        try:
            with default_storage.open(self.audio.name, 'rb') as fh:
                audio_data = io.BytesIO(fh.read())
            audio_info = mutagen.File(audio_data)
            if audio_info and hasattr(audio_info, 'info'):
                return int(audio_info.info.length)
        except Exception:
            pass
        return None

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def save(self, *args, **kwargs):
        if self.cover:
            # Preserve the existing cover name so the storage backend does
            # not generate a duplicate filename on re-save.
            file_name = self.cover.name
            if default_storage.exists(file_name):
                self.cover.name = file_name

        super().save(*args, **kwargs)

        if self.audio and not self.duration:
            duration = self._extract_duration()
            if duration:
                self.duration = duration
                super().save(update_fields=['duration'])

    def delete(self, *args, **kwargs):
        audio_name = self.audio.name if self.audio else None
        cover_name = self.cover.name if self.cover else None

        super().delete(*args, **kwargs)

        for name in filter(None, [audio_name, cover_name]):
            try:
                default_storage.delete(name)
            except Exception:
                pass
