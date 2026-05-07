from rest_framework import serializers

from orrin.models import PlaylistModel, Track


class PlaylistTrackSerializer(serializers.ModelSerializer):
    audio_url = serializers.SerializerMethodField()
    cover_url = serializers.SerializerMethodField()
    duration_formatted = serializers.CharField(read_only=True)
    artist_name = serializers.CharField(source='artist.name', read_only=True)
    artist_slug = serializers.CharField(source='artist.slug', read_only=True)

    class Meta:
        model = Track
        fields = [
            'slug',
            'title',
            'artist_name',
            'artist_slug',
            'duration',
            'duration_formatted',
            'cover_url',
            'audio_url',
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


class PlaylistSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    cover = serializers.SerializerMethodField()
    track_count = serializers.SerializerMethodField()
    total_duration = serializers.SerializerMethodField()

    class Meta:
        model = PlaylistModel
        fields = [
            'id',
            'slug',
            'title',
            'description',
            'cover',
            'visibility',
            'owner',
            'track_count',
            'total_duration',
            'created_at',
        ]
        read_only_fields = ['id', 'slug', 'owner', 'created_at']

    def get_owner(self, obj):
        return {
            'id': obj.owner.id,
            'username': obj.owner.username,
        }

    def get_cover(self, obj):
        request = self.context.get('request')
        if obj.cover and hasattr(obj.cover, 'url'):
            return request.build_absolute_uri(obj.cover.url)
        return None

    def get_track_count(self, obj):
        return obj.tracks.count()

    def get_total_duration(self, obj):
        return sum(t.duration or 0 for t in obj.tracks.only('duration'))


class PlaylistDetailSerializer(PlaylistSerializer):
    tracks = serializers.SerializerMethodField()

    class Meta(PlaylistSerializer.Meta):
        fields = PlaylistSerializer.Meta.fields + ['tracks']

    def get_tracks(self, obj):
        ordered_tracks = (
            obj.tracks
            .order_by('playlist_entries__order')
            .select_related('artist')
        )
        return PlaylistTrackSerializer(
            ordered_tracks,
            many=True,
            context=self.context,
        ).data


class PlaylistWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaylistModel
        fields = ['title', 'description', 'visibility', 'cover']

    def validate_title(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('Title cannot be blank.')
        return value.strip()
