from rest_framework import serializers

from library.models import FollowedArtist
from orrin.models import Artist


class FollowedArtistItemSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    genre = serializers.SerializerMethodField()

    class Meta:
        model = Artist
        fields = [
            "slug",
            "name",
            "image_url",
            "genre",
            "monthly_listeners",
            "mini_description",
        ]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None

    def get_genre(self, obj):
        first_genre = obj.genres.first()
        return first_genre.name if first_genre else None


class FollowedArtistSerializer(serializers.ModelSerializer):
    artist = FollowedArtistItemSerializer(read_only=True)
    followed_at = serializers.DateTimeField(source="created_at", read_only=True)

    class Meta:
        model = FollowedArtist
        fields = ["artist", "followed_at"]
