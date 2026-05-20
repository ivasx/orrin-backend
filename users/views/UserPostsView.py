from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from feed.models import Post
from feed.serializers import PostSerializer
from feed.views.FeedView import build_interaction_map

User = get_user_model()


class UserPostsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, username):
        user = get_object_or_404(User, username=username)

        posts = list(
            Post.objects
            .filter(author=user)
            .select_related('author', 'track', 'track__artist')
            .order_by('-created_at')
        )

        interaction_map = build_interaction_map(request.user, posts)

        serializer = PostSerializer(
            posts,
            many=True,
            context={'request': request, 'interaction_map': interaction_map},
        )
        return Response(serializer.data)