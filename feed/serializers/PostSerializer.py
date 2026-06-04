from django.utils.timesince import timesince
from rest_framework import serializers

from feed.models import Post, PostComment


class PostAuthorSerializer(serializers.Serializer):
    """
    Unified author shape consumed by the frontend.

    Both `isVerified` and `isArtist` are camelCase because the frontend
    uses these keys directly without a normaliser for post authors.
    """

    id = serializers.IntegerField()
    username = serializers.CharField()
    name = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    isVerified = serializers.BooleanField(source='is_verified')
    isArtist = serializers.SerializerMethodField()

    def get_name(self, obj):
        full = f'{obj.first_name} {obj.last_name}'.strip()
        return full or obj.username

    def get_avatar(self, obj):
        request = self.context.get('request')
        if obj.avatar and hasattr(obj.avatar, 'url'):
            return request.build_absolute_uri(obj.avatar.url) if request else obj.avatar.url
        return None

    def get_isArtist(self, obj):
        return obj.managed_artists.exists()


class AttachedTrackSerializer(serializers.Serializer):
    """
    Compact track shape attached to a post — matches the frontend's
    `attachedTrack` structure exactly.
    """

    trackId = serializers.CharField(source='slug')
    title = serializers.CharField()
    artist = serializers.CharField(source='artist.name')
    cover = serializers.SerializerMethodField()

    def get_cover(self, obj):
        request = self.context.get('request')
        if obj.cover and hasattr(obj.cover, 'url'):
            return request.build_absolute_uri(obj.cover.url) if request else obj.cover.url
        return None


class PostCommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    likes_count = serializers.IntegerField(default=0, read_only=True)

    class Meta:
        model = PostComment
        fields = ['id', 'author', 'text', 'created_at', 'likes_count']
        read_only_fields = ['id', 'author', 'created_at']

    def get_author(self, obj):
        request = self.context.get('request')
        avatar = None
        if obj.author.avatar and hasattr(obj.author.avatar, 'url'):
            avatar = (
                request.build_absolute_uri(obj.author.avatar.url)
                if request
                else obj.author.avatar.url
            )
        return {
            'id': obj.author.id,
            'username': obj.author.username,
            'name': (
                f'{obj.author.first_name} {obj.author.last_name}'.strip()
                or obj.author.username
            ),
            'avatar': avatar,
        }


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    attachedTrack = serializers.SerializerMethodField()
    timestamp = serializers.SerializerMethodField()
    fullTimestamp = serializers.DateTimeField(source='created_at', read_only=True)
    likesCount = serializers.SerializerMethodField()
    commentsCount = serializers.SerializerMethodField()
    repostsCount = serializers.SerializerMethodField()
    isLiked = serializers.SerializerMethodField()
    isReposted = serializers.SerializerMethodField()
    isSaved = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'text',
            'attachedTrack',
            'timestamp',
            'fullTimestamp',
            'likesCount',
            'commentsCount',
            'repostsCount',
            'isLiked',
            'isReposted',
            'isSaved',
        ]


    def get_author(self, obj):
        return PostAuthorSerializer(obj.author, context=self.context).data


    def get_attachedTrack(self, obj):
        if not obj.track:
            return None
        return AttachedTrackSerializer(obj.track, context=self.context).data


    def get_timestamp(self, obj):
        return timesince(obj.created_at).split(',')[0] + ' ago'


    def get_likesCount(self, obj):
        return obj.likes.count()

    def get_commentsCount(self, obj):
        return obj.comments.count()

    def get_repostsCount(self, obj):
        return obj.reposts.count()


    def _interaction_map(self):
        return self.context.get('interaction_map') or {}

    def get_isLiked(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        im = self._interaction_map()
        if im:
            return obj.id in im.get('liked', set())
        return obj.likes.filter(user=request.user).exists()

    def get_isReposted(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        im = self._interaction_map()
        if im:
            return obj.id in im.get('reposted', set())
        return obj.reposts.filter(user=request.user).exists()

    def get_isSaved(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        im = self._interaction_map()
        if im:
            return obj.id in im.get('saved', set())
        return obj.saves.filter(user=request.user).exists()


class PostWriteSerializer(serializers.ModelSerializer):
    track_slug = serializers.SlugField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Post
        fields = ['text', 'track_slug']

    def validate_text(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('Text cannot be blank.')
        return value.strip()

    def create(self, validated_data):
        from orrin.models import Track
        track_slug = validated_data.pop('track_slug', None)
        track = Track.objects.filter(slug=track_slug).first() if track_slug else None
        return Post.objects.create(track=track, **validated_data)

    def update(self, instance, validated_data):
        from orrin.models import Track
        track_slug = validated_data.pop('track_slug', ...)
        if track_slug is not ...:
            instance.track = (
                Track.objects.filter(slug=track_slug).first()
                if track_slug
                else None
            )
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance
