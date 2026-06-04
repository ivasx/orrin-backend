from rest_framework import serializers

from ..models import Artist, Track, Album


class BandMemberSerializer(serializers.Serializer):
    """Serialises a single BandMembership with the member's public profile."""

    id = serializers.IntegerField(source='member.id')
    name = serializers.CharField(source='member.name')
    role = serializers.CharField()
    image_url = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.member.image and hasattr(obj.member.image, 'url'):
            return (
                request.build_absolute_uri(obj.member.image.url)
                if request
                else obj.member.image.url
            )
        return None


class AlbumBriefSerializer(serializers.ModelSerializer):
    """Compact album representation used inside an artist's discography list."""

    cover_url = serializers.SerializerMethodField()
    type = serializers.CharField(source='album_type')

    class Meta:
        model = Album
        fields = ['id', 'slug', 'title', 'year', 'type', 'cover_url']

    def get_cover_url(self, obj):
        request = self.context.get('request')
        if obj.cover and hasattr(obj.cover, 'url'):
            return (
                request.build_absolute_uri(obj.cover.url)
                if request
                else obj.cover.url
            )
        return None



class ArtistTrackSerializer(serializers.ModelSerializer):
    cover_url = serializers.SerializerMethodField()
    audio_url = serializers.SerializerMethodField()
    duration_formatted = serializers.SerializerMethodField()
    artist_name = serializers.CharField(source='artist.name', read_only=True)
    artist_slug = serializers.CharField(source='artist.slug', read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Track
        fields = [
            'id',
            'slug',
            'title',
            'artist_name',
            'artist_slug',
            'duration',
            'duration_formatted',
            'cover_url',
            'audio_url',
            'plays_count',
            'is_liked',
        ]

    def get_duration_formatted(self, obj):
        return obj.duration_formatted()

    def get_cover_url(self, obj):
        request = self.context.get('request')
        if obj.cover and hasattr(obj.cover, 'url'):
            return request.build_absolute_uri(obj.cover.url) if request else obj.cover.url
        return None

    def get_audio_url(self, obj):
        request = self.context.get('request')
        if obj.audio and hasattr(obj.audio, 'url'):
            return request.build_absolute_uri(obj.audio.url) if request else obj.audio.url
        return None

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        liked_ids = self.context.get('liked_ids')
        if liked_ids is not None:
            return obj.id in liked_ids
        from library.models import LikedTrack
        return LikedTrack.objects.filter(user=request.user, track=obj).exists()



class SimilarArtistSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Artist
        fields = ['id', 'slug', 'name', 'image_url', 'monthly_listeners', 'is_verified']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None



class ArtistSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    genres = serializers.SlugRelatedField(many=True, read_only=True, slug_field='slug')

    class Meta:
        model = Artist
        fields = [
            'id',
            'name',
            'slug',
            'type',
            'genres',
            'about',
            'history',
            'location',
            'join_date',
            'monthly_listeners',
            'mini_description',
            'image',
            'image_url',
            'socials',
            'is_verified',
        ]

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None



class ArtistDetailSerializer(ArtistSerializer):
    popular_tracks = serializers.SerializerMethodField()
    discography = serializers.SerializerMethodField()
    members = serializers.SerializerMethodField()
    similar_artists = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

    class Meta(ArtistSerializer.Meta):
        fields = ArtistSerializer.Meta.fields + [
            'popular_tracks',
            'discography',
            'members',
            'similar_artists',
            'followers_count',
            'is_following',
        ]


    def get_popular_tracks(self, obj):
        from django.db.models import F
        tracks = (
            obj.tracks
            .select_related('artist')
            .order_by(F('plays_count').desc(nulls_last=True))[:10]
        )
        liked_ids = self._get_liked_ids(tracks)
        return ArtistTrackSerializer(
            tracks,
            many=True,
            context={**self.context, 'liked_ids': liked_ids},
        ).data


    def get_discography(self, obj):
        albums = (
            obj.albums
            .prefetch_related('tracks')
            .order_by('-year', 'title')
        )
        return AlbumBriefSerializer(albums, many=True, context=self.context).data


    def get_members(self, obj):
        if obj.type != 'group':
            return []
        memberships = (
            obj.members
            .select_related('member')
            .filter(member__type='person')
        )
        return BandMemberSerializer(memberships, many=True, context=self.context).data


    def get_similar_artists(self, obj):
        genre_ids = obj.genres.values_list('id', flat=True)
        similar = (
            Artist.objects
            .filter(genres__in=genre_ids)
            .exclude(pk=obj.pk)
            .distinct()
            .order_by('-monthly_listeners')[:6]
        )
        return SimilarArtistSerializer(similar, many=True, context=self.context).data


    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_is_following(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return obj.followers.filter(user=request.user).exists()


    def _get_liked_ids(self, tracks):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return set()
        from library.models import LikedTrack
        track_ids = [t.id for t in tracks]
        return set(
            LikedTrack.objects
            .filter(user=request.user, track_id__in=track_ids)
            .values_list('track_id', flat=True)
        )
