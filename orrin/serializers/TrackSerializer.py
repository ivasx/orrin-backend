from rest_framework import serializers

from library.models import LikedTrack
from .ArtistSerializer import ArtistSerializer
from ..models import Track


class LyricLineSerializer(serializers.Serializer):
    time = serializers.FloatField(source='time_seconds')
    text = serializers.CharField()


class LyricsSerializer(serializers.Serializer):
    """
    Normalises Lyrics + LyricLine into the shape the frontend expects:

        { type: 'static',  content: "plain text..." }
        { type: 'synced',  content: [{time, text}, ...] }
    """
    type = serializers.CharField(source='lyrics_type')
    content = serializers.SerializerMethodField()

    def get_content(self, obj):
        if obj.lyrics_type == 'synced':
            return LyricLineSerializer(obj.lines.all(), many=True).data
        return obj.plain_text


class TrackSerializer(serializers.ModelSerializer):
    audio_url = serializers.SerializerMethodField()
    cover_url = serializers.SerializerMethodField()
    duration_formatted = serializers.SerializerMethodField()
    artist = ArtistSerializer(read_only=True)
    lyrics = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Track
        fields = [
            'id',
            'slug',
            'title',
            'artist',
            'duration',
            'duration_formatted',
            'cover_url',
            'audio_url',
            'plays_count',
            'lyrics',
            'is_liked',
        ]

    def get_duration_formatted(self, obj):
        return obj.duration_formatted()

    def get_audio_url(self, obj):
        request = self.context.get('request')
        if obj.audio and hasattr(obj.audio, 'url'):
            return request.build_absolute_uri(obj.audio.url) if request else obj.audio.url
        return None

    def get_cover_url(self, obj):
        request = self.context.get('request')
        if obj.cover and hasattr(obj.cover, 'url'):
            return request.build_absolute_uri(obj.cover.url) if request else obj.cover.url
        return None

    def get_lyrics(self, obj):
        try:
            return LyricsSerializer(obj.lyrics).data
        except Track.lyrics.RelatedObjectDoesNotExist:
            return None

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        # Prefer pre-fetched set injected by the view to avoid N+1
        liked_ids = self.context.get('liked_ids')
        if liked_ids is not None:
            return obj.id in liked_ids
        return LikedTrack.objects.filter(user=request.user, track=obj).exists()
