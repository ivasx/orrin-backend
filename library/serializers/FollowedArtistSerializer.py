from rest_framework import serializers

from library.models import FollowedArtist
from orrin.models import Artist


class FollowedArtistSerializer(serializers.ModelSerializer):
    """
    Returns a flat artist shape that matches the frontend contract
    consumed by ArtistsTab and ArtistCard:

        { id, slug, name, imageUrl, genre, monthly_listeners, is_verified }

    Previously this returned a nested { artist: {...}, followed_at: ... }
    shape which required extra mapping on the frontend.
    """

    id = serializers.IntegerField(source='artist.id', read_only=True)
    slug = serializers.SlugField(source='artist.slug', read_only=True)
    name = serializers.CharField(source='artist.name', read_only=True)
    imageUrl = serializers.SerializerMethodField()
    genre = serializers.SerializerMethodField()
    monthly_listeners = serializers.IntegerField(source='artist.monthly_listeners', read_only=True)
    is_verified = serializers.BooleanField(source='artist.is_verified', read_only=True)
    followed_at = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = FollowedArtist
        fields = [
            'id',
            'slug',
            'name',
            'imageUrl',
            'genre',
            'monthly_listeners',
            'is_verified',
            'followed_at',
        ]

    def get_imageUrl(self, obj):
        request = self.context.get('request')
        if obj.artist.image and hasattr(obj.artist.image, 'url'):
            return (
                request.build_absolute_uri(obj.artist.image.url)
                if request
                else obj.artist.image.url
            )
        return None

    def get_genre(self, obj):
        first = obj.artist.genres.first()
        return first.name if first else None
