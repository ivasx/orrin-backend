from django.db import models

from .SluggedModel import SluggedModel


class Album(SluggedModel):
    """
    Represents a music album or release.

    A track can exist independently of any album (single not attached to a release),
    or belong to one or more albums via the AlbumTrack through-table.
    """

    ALBUM_TYPE_CHOICES = (
        ('album', 'Album'),
        ('ep', 'EP'),
        ('single', 'Single'),
        ('compilation', 'Compilation'),
    )

    slug_source_fields = ['title', 'artist']

    title = models.CharField(max_length=255, verbose_name='Title')
    artist = models.ForeignKey(
        'Artist',
        on_delete=models.CASCADE,
        related_name='albums',
        verbose_name='Artist',
    )
    cover = models.ImageField(
        upload_to='images/albums/',
        blank=True,
        null=True,
        verbose_name='Cover image',
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Release year',
        null=True,
        blank=True,
    )
    album_type = models.CharField(
        max_length=15,
        choices=ALBUM_TYPE_CHOICES,
        default='album',
        verbose_name='Release type',
    )
    tracks = models.ManyToManyField(
        'Track',
        through='AlbumTrack',
        related_name='albums',
        blank=True,
    )

    class Meta:
        ordering = ('-year', 'title')

    def __str__(self):
        return f'{self.artist} — {self.title} ({self.year})'


class AlbumTrack(models.Model):
    """Ordered mapping between an album and its tracks."""

    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name='album_tracks',
    )
    track = models.ForeignKey(
        'Track',
        on_delete=models.CASCADE,
        related_name='album_entries',
    )
    track_number = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Track number',
    )

    class Meta:
        ordering = ('track_number',)
        unique_together = ('album', 'track')

    def __str__(self):
        return f'{self.album} — #{self.track_number} {self.track}'
