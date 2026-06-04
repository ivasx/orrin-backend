from rest_framework import serializers

from ..models import Album, AlbumTrack, Track


class AlbumTrackSerializer(serializers.ModelSerializer):
    """Ordered track entry inside an album detail response."""

    audio_url = serializers.SerializerMethodField()
    cover_url = serializers.SerializerMethodField()
    duration_formatted = serializers.SerializerMethodField()
    artist_name = serializers.CharField(source='artist.name', read_only=True)
    artist_slug = serializers.CharField(source='artist.slug', read_only=True)
    track_number = serializers.SerializerMethodField()

    class Meta:
        model = Track
        fields = [
            'id',
            'slug',
            'title',
            'artist_name',
            'artist_slug',
            'track_number',
            'duration',
            'duration_formatted',
            'cover_url',
            'audio_url',
            'plays_count',
        ]

    def get_track_number(self, obj):
        # AlbumTrack through-object is annotated in the view queryset
        return getattr(obj, 'track_number', None)

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


class AlbumListSerializer(serializers.ModelSerializer):
    """Compact representation for lists (discography, saved albums)."""

    cover_url = serializers.SerializerMethodField()
    artist_name = serializers.CharField(source='artist.name', read_only=True)
    artist_slug = serializers.CharField(source='artist.slug', read_only=True)
    track_count = serializers.SerializerMethodField()
    type = serializers.CharField(source='album_type')

    class Meta:
        model = Album
        fields = [
            'id',
            'slug',
            'title',
            'artist_name',
            'artist_slug',
            'year',
            'type',
            'cover_url',
            'track_count',
        ]

    def get_cover_url(self, obj):
        request = self.context.get('request')
        if obj.cover and hasattr(obj.cover, 'url'):
            return request.build_absolute_uri(obj.cover.url) if request else obj.cover.url
        return None

    def get_track_count(self, obj):
        return obj.tracks.count()


class AlbumDetailSerializer(AlbumListSerializer):
    """Full album with ordered track list."""

    tracks = serializers.SerializerMethodField()

    class Meta(AlbumListSerializer.Meta):
        fields = AlbumListSerializer.Meta.fields + ['tracks']

    def get_tracks(self, obj):
        ordered = (
            obj.tracks
            .order_by('album_entries__track_number')
            .select_related('artist')
        )
        # Annotate track_number so AlbumTrackSerializer can read it
        through_map = {
            at.track_id: at.track_number
            for at in AlbumTrack.objects.filter(album=obj)
        }
        for track in ordered:
            track.track_number = through_map.get(track.id)
        return AlbumTrackSerializer(ordered, many=True, context=self.context).data


class AlbumWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['title', 'album_type', 'year', 'cover']

    def validate_title(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('Title cannot be blank.')
        return value.strip()
