from rest_framework import serializers

from notes.models import Note, NoteLike


class LyricLineReferenceSerializer(serializers.Serializer):
    text = serializers.CharField(source='lyric_line.text', default=None)
    time = serializers.FloatField(source='lyric_line.time_seconds', default=None)


class NoteAuthorSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    name = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    def get_name(self, obj):
        full = f'{obj.first_name} {obj.last_name}'.strip()
        return full or obj.username

    def get_avatar(self, obj):
        request = self.context.get('request')
        if obj.avatar and hasattr(obj.avatar, 'url'):
            return request.build_absolute_uri(obj.avatar.url) if request else obj.avatar.url
        return None


class NoteSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    likesCount = serializers.SerializerMethodField()
    isLikedByMe = serializers.SerializerMethodField()
    lyricsLineReference = serializers.SerializerMethodField()
    timecode = serializers.SerializerMethodField()
    type = serializers.CharField(source='note_type')
    timestamp = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = Note
        fields = [
            'id',
            'author',
            'text',
            'type',
            'timestamp',
            'timecode',
            'likesCount',
            'isLikedByMe',
            'lyricsLineReference',
        ]

    def get_author(self, obj):
        return NoteAuthorSerializer(obj.author, context=self.context).data

    def get_likesCount(self, obj):
        return obj.likes.count()

    def get_isLikedByMe(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        liked_note_ids = self.context.get('liked_note_ids')
        if liked_note_ids is not None:
            return obj.id in liked_note_ids
        return obj.likes.filter(user=request.user).exists()

    def get_lyricsLineReference(self, obj):
        if obj.lyric_line_id is None:
            return None
        return {
            'text': obj.lyric_line.text,
            'time': obj.lyric_line.time_seconds,
        }

    def get_timecode(self, obj):
        if obj.timecode is None:
            return None
        # Return as "M:SS" string matching the frontend format
        total = int(obj.timecode)
        minutes, seconds = divmod(total, 60)
        return f'{minutes}:{seconds:02d}'


class NoteWriteSerializer(serializers.ModelSerializer):
    track_slug = serializers.SlugField(write_only=True, required=False, allow_null=True)
    artist_slug = serializers.SlugField(write_only=True, required=False, allow_null=True)
    lyric_line_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Note
        fields = [
            'text',
            'note_type',
            'timecode',
            'track_slug',
            'artist_slug',
            'lyric_line_id',
        ]

    def validate(self, attrs):
        if not attrs.get('track_slug') and not attrs.get('artist_slug'):
            raise serializers.ValidationError(
                'A note must reference at least a track or an artist.'
            )
        return attrs

    def create(self, validated_data):
        from orrin.models import Track, Artist, LyricLine

        track_slug = validated_data.pop('track_slug', None)
        artist_slug = validated_data.pop('artist_slug', None)
        lyric_line_id = validated_data.pop('lyric_line_id', None)

        track = Track.objects.filter(slug=track_slug).first() if track_slug else None
        artist = Artist.objects.filter(slug=artist_slug).first() if artist_slug else None
        lyric_line = (
            LyricLine.objects.filter(id=lyric_line_id).first()
            if lyric_line_id
            else None
        )

        return Note.objects.create(
            track=track,
            artist=artist,
            lyric_line=lyric_line,
            **validated_data,
        )
