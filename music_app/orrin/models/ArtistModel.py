from django.db import models


class Artist(models.Model):
    """
    Represents an artist entity, which can be either a solo performer, a music group, or a band member.
    """
    ARTIST_TYPE_CHOICES  = (
        ('group', 'Group'),
        ('person', 'Person'),
    )

    type = models.CharField(max_length=10, choices=ARTIST_TYPE_CHOICES, default='person', verbose_name='Type')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Slug')

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

    def __str__(self):
        return f'{self.name} - {self.mini_description}'




