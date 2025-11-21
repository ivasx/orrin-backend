from django.conf import settings
from django.db import models

from orrin.models import SluggedModel


class PlaylistModel(SluggedModel):
    PLAYLIST_TYPE_CHOICES = (
        ('public', 'Public'),
        ('friends', 'For Friends'),
        ('private', 'Private'),
    )
    slug_source_fields = ['title',]

    title = models.CharField(max_length=255, verbose_name='Title')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name = 'playlists',
        verbose_name='Owner'
    )
    cover = models.ImageField(upload_to='images/playlists/', blank=True, null=True)
    visibility = models.CharField(max_length=10, choices=PLAYLIST_TYPE_CHOICES, default='public', verbose_name='Visibility')
    tracks = models.ManyToManyField('Track', through='PlaylistTrack' ,related_name='playlists')

    def __str__(self):
        return self.title

