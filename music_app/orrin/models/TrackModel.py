import os
from django.core.files.storage import default_storage
from django.db import models
from django.urls import reverse
from slugify import slugify
from orrin.models import Artist


class Track(models.Model):
    """
    Represents a music track with metadata and media files.

    The class is a Django model used to define and handle the metadata and
    media files associated with a music track. It includes fields for storing
    the title, artist, cover image, and audio file. It also defines utilities
    to manage the object's slug, formatted duration, absolute URL, and safe
    deletion of its media files.
    """

    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Slug')
    title = models.CharField(max_length=255, verbose_name='Title')
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, verbose_name='Artist', related_name='tracks')
    cover = models.ImageField(upload_to='images/covers/', blank=True, null=True, verbose_name='Обкладинка')
    audio = models.FileField(upload_to='audio/', blank=True, null=True, verbose_name='Аудіо файл')

    duration = models.PositiveIntegerField(
        help_text="Тривалість треку у секундах",
        blank=True, default=0, null=True,
        verbose_name='Тривалість',
    )

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

    def save(self, *args, **kwargs):
        # If slug is not provided, generate it from title and artist
        if not self.slug:
            base_slug = slugify(f'{self.title}-{self.artist}')
            slug = base_slug
            num = 1
            while Track.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{num}'
                num += 1
            self.slug = slug

        if self.cover:
            file_name = self.cover.name
            if default_storage.exists(file_name):
                self.cover.name = file_name
            else:
                pass

        super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        if self.audio:
            if os.path.exists(self.audio.path):
                os.remove(self.audio.path)
        if self.cover:
            if os.path.exists(self.cover.path):
                os.remove(self.cover.path)
        super().delete(*args, **kwargs)