from rest_framework import serializers

from orrin.serializers.ArtistSerializer import ArtistSerializer
from library.models import FollowedArtist


class FollowedArtistSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)
    followed_at = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = FollowedArtist
        fields = ['artist', 'followed_at']
