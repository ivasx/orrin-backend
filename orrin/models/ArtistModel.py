from django.db import models
from .SluggedModel import SluggedModel
from django.conf import settings

class Artist(SluggedModel):
    """
    Represents an artist entity, which can be either a solo performer, a music group, or a band member.
    """

    ARTIST_TYPE_CHOICES  = (
        ('group', 'Group'),
        ('person', 'Person'),
    )

    type = models.CharField(max_length=10, choices=ARTIST_TYPE_CHOICES, default='person', verbose_name='Type')
    managers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='managed_artists',
        blank=True,
        verbose_name='Managers'
    )

    # slug = generated in the base class SluggedModel

    name = models.CharField(max_length=255, verbose_name='Name')
    mini_description = models.CharField(max_length=255, blank=True, null=True, verbose_name='Short description or tagline')
    genres = models.ManyToManyField('Genre', related_name='artists', verbose_name='Genres')
    monthly_listeners = models.PositiveIntegerField(default=0, verbose_name='Number of listeners per month')
    image = models.ImageField(upload_to='images/artists/', blank=True, null=True, verbose_name='Photo')
    about = models.TextField(blank=True, null=True, verbose_name='About')
    history = models.TextField(blank=True, null=True, verbose_name='History')
    location = models.CharField(max_length=255, blank=True, null=True, verbose_name='Location')
    join_date = models.CharField(max_length=50, blank=True, null=True, verbose_name='Join date (Start career)')
    socials = models.JSONField(default=dict, blank=True)

    slug_source_fields = ['name']

    @property
    def is_solo_artist(self):
        return self.tracks.exists()

    def get_group_tracks(self):
        from .TrackModel import Track
        if self.type != 'person':
            return Track.objects.none()

        group_ids = self.band_memberships.values_list('group_id', flat=True)

        return Track.objects.filter(artist_id__in=group_ids).order_by('-id')

    def __str__(self):
        return f'{self.name}'




