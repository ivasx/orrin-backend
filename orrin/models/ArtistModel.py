from django.conf import settings
from django.db import models

from .SluggedModel import SluggedModel


class Artist(SluggedModel):
    """
    Represents an artist entity — either a solo performer or a music group.

    Solo performers (type='person') can be linked to groups via BandMembership.
    Groups (type='group') aggregate members through the same relation.
    """

    ARTIST_TYPE_CHOICES = (
        ('group', 'Group'),
        ('person', 'Person'),
    )

    slug_source_fields = ['name']

    type = models.CharField(
        max_length=10,
        choices=ARTIST_TYPE_CHOICES,
        default='person',
        verbose_name='Type',
    )
    managers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='managed_artists',
        blank=True,
        verbose_name='Managers',
    )
    name = models.CharField(max_length=255, verbose_name='Name')
    mini_description = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Short description or tagline',
    )
    genres = models.ManyToManyField(
        'Genre',
        related_name='artists',
        verbose_name='Genres',
        blank=True,
    )
    monthly_listeners = models.PositiveIntegerField(
        default=0,
        verbose_name='Monthly listeners',
    )
    image = models.ImageField(
        upload_to='images/artists/',
        blank=True,
        null=True,
        verbose_name='Photo',
    )
    about = models.TextField(blank=True, null=True, verbose_name='About')
    history = models.TextField(blank=True, null=True, verbose_name='History')
    location = models.CharField(max_length=255, blank=True, null=True, verbose_name='Location')
    join_date = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Career start year',
    )
    socials = models.JSONField(default=dict, blank=True)
    is_verified = models.BooleanField(
        default=False,
        verbose_name='Verified',
        help_text='Designates whether this artist profile has been officially verified.',
    )

    def __str__(self):
        return self.name
