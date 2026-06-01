import io
import mutagen
from django.core.files.storage import default_storage
from django.db import models
from django.urls import reverse
from .SluggedModel import SluggedModel


class Track(SluggedModel):
    """
    Represents a music track with metadata and media files.

    The class is a Django model used to define and handle the metadata and
    media files associated with a music track. It includes fields for storing
    the title, artist, cover image, and audio file. It also defines utilities
    to manage the object's slug, formatted duration, absolute URL, and safe
    deletion of its media files.
    """

    # slug = generated in the base class SluggedModel
    title = models.CharField(max_length=255, verbose_name='Title')
    artist = models.ForeignKey('Artist', on_delete=models.CASCADE, verbose_name='Artist', related_name='tracks')
    cover = models.ImageField(upload_to='images/covers/', blank=True, null=True, verbose_name='Cover image')
    audio = models.FileField(upload_to='audio/', blank=True, null=True, verbose_name='Audio file')
    duration = models.PositiveIntegerField(
        help_text="Тривалість треку у секундах",
        blank=True, default=0, null=True,
        verbose_name='Тривалість',
    )

    slug_source_fields = ['title', 'artist']

    def __str__(self):
        return f'{self.title} - {self.artist}'

    def duration_formatted(self):
        if not self.duration:
            return "0:00"
        minutes = self.duration // 60
        seconds = self.duration % 60
        return f'{minutes}:{seconds:02}'

    def get_absolute_url(self):
        return reverse('track-detail-api', kwargs={'slug': self.slug})

    def _extract_duration(self):
        try:
            with default_storage.open(self.audio.name, 'rb') as f:
                audio_data = io.BytesIO(f.read())
            audio_info = mutagen.File(audio_data)
            if audio_info and hasattr(audio_info, 'info'):
                return int(audio_info.info.length)
        except Exception:
            pass
        return None

    def save(self, *args, **kwargs):
        if self.cover:
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

        if audio_name:
            try:
                default_storage.delete(audio_name)
            except Exception:
                pass

        if cover_name:
            try:
                default_storage.delete(cover_name)
            except Exception:
                pass