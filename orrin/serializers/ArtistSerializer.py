from rest_framework import serializers

from ..models import Artist, Track


class ArtistTrackSerializer(serializers.ModelSerializer):
    cover_url = serializers.SerializerMethodField()
    audio_url = serializers.SerializerMethodField()
    duration_formatted = serializers.SerializerMethodField()
    artist_name = serializers.CharField(source="artist.name", read_only=True)
    artist_slug = serializers.CharField(source="artist.slug", read_only=True)

    class Meta:
        model = Track
        fields = [
            "slug",
            "title",
            "artist_name",
            "artist_slug",
            "duration",
            "duration_formatted",
            "cover_url",
            "audio_url",
        ]

    def get_duration_formatted(self, obj):
        return obj.duration_formatted()

    def get_cover_url(self, obj):
        request = self.context.get("request")
        if obj.cover and hasattr(obj.cover, "url"):
            return request.build_absolute_uri(obj.cover.url) if request else obj.cover.url
        return None

    def get_audio_url(self, obj):
        request = self.context.get("request")
        if obj.audio and hasattr(obj.audio, "url"):
            return request.build_absolute_uri(obj.audio.url) if request else obj.audio.url
        return None


class SimilarArtistSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Artist
        fields = ["slug", "name", "image_url", "monthly_listeners"]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None


class ArtistSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    genres = serializers.SlugRelatedField(many=True, read_only=True, slug_field="slug")

    class Meta:
        model = Artist
        fields = [
            "id",
            "name",
            "slug",
            "type",
            "genres",
            "about",
            "history",
            "location",
            "join_date",
            "monthly_listeners",
            "mini_description",
            "image",
            "image_url",
            "socials",
        ]


class ArtistDetailSerializer(ArtistSerializer):
    popular_tracks = serializers.SerializerMethodField()
    similar_artists = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

    class Meta(ArtistSerializer.Meta):
        fields = ArtistSerializer.Meta.fields + [
            "popular_tracks",
            "similar_artists",
            "followers_count",
            "is_following",
        ]

    def get_popular_tracks(self, obj):
        from library.models import ListeningHistory
        from django.db.models import Count

        track_qs = (
            obj.tracks
            .annotate(play_count=Count("history_entries"))
            .order_by("-play_count", "-id")[:10]
            .select_related("artist")
        )
        return ArtistTrackSerializer(track_qs, many=True, context=self.context).data

    def get_similar_artists(self, obj):
        genre_ids = obj.genres.values_list("id", flat=True)
        similar = (
            Artist.objects
            .filter(genres__in=genre_ids)
            .exclude(pk=obj.pk)
            .distinct()
            .order_by("-monthly_listeners")[:6]
        )
        return SimilarArtistSerializer(similar, many=True, context=self.context).data

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_is_following(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        return obj.followers.filter(user=request.user).exists()

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None
