from rest_framework import serializers

from orrin.models import Track
from orrin.serializers.ArtistSerializer import ArtistSerializer
from library.models import LikedTrack


class LibraryTrackSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)
    audio_url = serializers.SerializerMethodField()
    cover_url = serializers.SerializerMethodField()
    duration_formatted = serializers.CharField(read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Track
        fields = [
            'slug',
            'title',
            'artist',
            'duration',
            'duration_formatted',
            'cover_url',
            'audio_url',
            'is_liked',
        ]

    def get_audio_url(self, obj):
        request = self.context.get('request')
        if obj.audio and hasattr(obj.audio, 'url'):
            return request.build_absolute_uri(obj.audio.url)
        return None

    def get_cover_url(self, obj):
        request = self.context.get('request')
        if obj.cover and hasattr(obj.cover, 'url'):
            return request.build_absolute_uri(obj.cover.url)
        return None

    def get_is_liked(self, obj):
        user = self.context.get('request').user
        if not user or not user.is_authenticated:
            return False
        liked_ids = self.context.get('liked_ids')
        if liked_ids is not None:
            return obj.id in liked_ids
        return LikedTrack.objects.filter(user=user, track=obj).exists()
