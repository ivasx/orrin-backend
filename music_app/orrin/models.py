from django.db import models
from django.urls import reverse
from slugify import slugify
from mutagen import File


# Create your models here.
class Track(models.Model):
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Слаг')
    title = models.CharField(max_length=50, verbose_name='Назва')
    artist = models.CharField(max_length=50, verbose_name='Виконавець')
    cover = models.ImageField(upload_to='images/covers/', blank=True, null=True, verbose_name='Обложка')
    audio = models.FileField(upload_to='audio/', blank=True, null=True, verbose_name='Аудіо')
    duration = models.PositiveIntegerField(
        help_text="Тривалість треку у секундах",
        blank=True, default=0, null=True,
        verbose_name='Тривалість',
    )

    def __str__(self):
        return f'{self.title} - {self.artist}'

    def duration_formatted(self):
        minutes = self.duration // 60
        seconds = self.duration % 60
        return f'{minutes}:{seconds:02}'

    def get_absolute_url(self):
        return reverse('track_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        base_slug = slugify(f'{self.title}-{self.artist}')
        slug = base_slug
        num = 1
        while Track.objects.filter(slug=slug).exists():
            slug = f'{base_slug}-{num}'
            num += 1
        self.slug = slug

        if self.audio:
            audio_file = File(self.audio)
            if audio_file:
                self.duration = int(audio_file.info.length)

        super().save(*args, **kwargs)
