from django.db import models


class Genre(models.Model):
    """
    Represents a genre of music.
    """

    name = models.CharField(max_length=255, unique=True, verbose_name='Name')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Slug')

    def __str__(self):
        return self.name