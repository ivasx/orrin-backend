from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(read_only=True)
    following_count = serializers.IntegerField(read_only=True)
    managed_artists = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    avatar_url = serializers.SerializerMethodField()
    cover_photo_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "name",
            "bio",
            "avatar",
            "avatar_url",
            "cover_photo",
            "cover_photo_url",
            "date_of_birth",
            "gender",
            "location",
            "website",
            "followers_count",
            "following_count",
            "date_joined",
            "managed_artists",
            "is_following",
        )
        read_only_fields = ("id", "email", "date_joined")
        extra_kwargs = {
            "avatar": {"write_only": True, "required": False, "allow_null": True},
            "cover_photo": {"write_only": True, "required": False, "allow_null": True},
            "username": {"required": False},
        }

    def validate_username(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Username cannot be blank.")
        qs = User.objects.filter(username=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def get_name(self, obj):
        full = f"{obj.first_name} {obj.last_name}".strip()
        return full or obj.username

    def get_managed_artists(self, obj):
        return list(obj.managed_artists.values_list("slug", flat=True))

    def get_is_following(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        return obj.followers.filter(id=request.user.id).exists()

    def get_avatar_url(self, obj):
        request = self.context.get("request")
        if obj.avatar and hasattr(obj.avatar, "url"):
            return request.build_absolute_uri(obj.avatar.url) if request else obj.avatar.url
        return None

    def get_cover_photo_url(self, obj):
        request = self.context.get("request")
        if obj.cover_photo and hasattr(obj.cover_photo, "url"):
            return request.build_absolute_uri(obj.cover_photo.url) if request else obj.cover_photo.url
        return None


class UserCompactSerializer(serializers.ModelSerializer):
    is_following = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "username", "name", "first_name", "last_name", "avatar_url", "is_following")

    def get_name(self, obj):
        full = f"{obj.first_name} {obj.last_name}".strip()
        return full or obj.username

    def get_is_following(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        return obj.followers.filter(id=request.user.id).exists()

    def get_avatar_url(self, obj):
        request = self.context.get("request")
        if obj.avatar and hasattr(obj.avatar, "url"):
            return request.build_absolute_uri(obj.avatar.url) if request else obj.avatar.url
        return None
