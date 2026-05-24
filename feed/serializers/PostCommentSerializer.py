from rest_framework import serializers

from feed.models import PostComment


class PostCommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = PostComment
        fields = ['id', 'author', 'text', 'created_at']
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
            'avatar': avatar,
        }