from rest_framework import serializers

from feed.models import Post
from feed.serializers.PostCommentSerializer import PostCommentSerializer


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    track = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    reposts_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_reposted = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'author', 'text', 'track', 'created_at', 'updated_at',
            'likes_count', 'reposts_count', 'comments_count',
            'is_liked', 'is_reposted', 'is_saved',
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

    def get_author(self, obj):
        return {
            'id': obj.author.id,
            'username': obj.author.username,
            'avatar': obj.author.avatar.url if obj.author.avatar else None,
        }

    def get_track(self, obj):
        if not obj.track:
            return None
        request = self.context.get('request')
        return {
            'slug': obj.track.slug,
            'title': obj.track.title,
            'artist': obj.track.artist.name,
            'cover_url': request.build_absolute_uri(obj.track.cover.url) if obj.track.cover else None,
        }

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_reposts_count(self, obj):
        return obj.reposts.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

    def _get_user(self):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user
        return None

    def get_is_liked(self, obj):
        user = self._get_user()
        if not user:
            return False
        interaction_map = self.context.get('interaction_map')
        if interaction_map is not None:
            return obj.id in interaction_map.get('liked', set())
        return obj.likes.filter(user=user).exists()

    def get_is_reposted(self, obj):
        user = self._get_user()
        if not user:
            return False
        interaction_map = self.context.get('interaction_map')
        if interaction_map is not None:
            return obj.id in interaction_map.get('reposted', set())
        return obj.reposts.filter(user=user).exists()

    def get_is_saved(self, obj):
        user = self._get_user()
        if not user:
            return False
        interaction_map = self.context.get('interaction_map')
        if interaction_map is not None:
            return obj.id in interaction_map.get('saved', set())
        return obj.saves.filter(user=user).exists()


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
            instance.track = Track.objects.filter(slug=track_slug).first() if track_slug else None
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance
