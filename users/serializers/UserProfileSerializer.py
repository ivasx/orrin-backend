from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(read_only=True)
    following_count = serializers.IntegerField(read_only=True)
    managed_artists = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'bio', 'avatar', 'cover_photo', 'date_of_birth',
            'gender', 'location', 'website',
            'followers_count', 'following_count', 'date_joined',
            'managed_artists'
        )
        read_only_fields = ('id', 'username', 'email', 'date_joined')

    def get_managed_artists(self, obj):
        # Fetch only the 'slug' field from the managed_artists relation for performance
        return list(obj.managed_artists.values_list('slug', flat=True))