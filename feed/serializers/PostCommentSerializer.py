from rest_framework import serializers

from feed.models import PostComment


class PostCommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = PostComment
        fields = ['id', 'author', 'text', 'created_at']
        read_only_fields = ['id', 'author', 'created_at']

    def get_author(self, obj):
        return {
            'id': obj.author.id,
            'username': obj.author.username,
            'avatar': obj.author.avatar.url if obj.author.avatar else None,
        }
