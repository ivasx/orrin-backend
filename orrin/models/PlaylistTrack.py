from django.db import models


class PlaylistTrack(models.Model):
    playlist = models.ForeignKey('PlaylistModel', on_delete=models.CASCADE, related_name='tracks')
    track = models.ForeignKey('Track', on_delete=models.CASCADE, related_name='playlists')
    order = models.PositiveIntegerField(default=0, verbose_name='Order in playlist')
    added_date = models.DateTimeField(auto_now_add=True, verbose_name='Added date')

    class Meta:
        ordering = ('order',)