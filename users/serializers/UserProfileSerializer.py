from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(read_only=True)
    following_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'bio', 'avatar', 'cover_photo', 'date_of_birth',
            'gender', 'location', 'website',
            'followers_count', 'following_count', 'date_joined'
        )
        read_only_fields = ('id', 'username', 'email', 'date_joined')