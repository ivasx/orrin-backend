from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(read_only=True)
    following_count = serializers.IntegerField(read_only=True)
    managed_artists = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'name',
            'bio',
            'avatar',
            'cover_photo',
            'date_of_birth',
            'gender',
            'location',
            'website',
            'followers_count',
            'following_count',
            'date_joined',
            'managed_artists',
            'is_following',
        )
        read_only_fields = ('id', 'username', 'email', 'date_joined')

    def get_name(self, obj):
        full = f"{obj.first_name} {obj.last_name}".strip()
        return full or obj.username

    def get_managed_artists(self, obj):
        return list(obj.managed_artists.values_list('slug', flat=True))

    def get_is_following(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return obj.followers.filter(id=request.user.id).exists()


class UserCompactSerializer(serializers.ModelSerializer):
    is_following = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'name', 'first_name', 'last_name', 'avatar', 'is_following')

    def get_name(self, obj):
        full = f"{obj.first_name} {obj.last_name}".strip()
        return full or obj.username

    def get_is_following(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return obj.followers.filter(id=request.user.id).exists()
