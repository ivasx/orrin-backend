from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from orrin.models import Artist
from feed.models import Post
from feed.serializers import PostSerializer
from feed.views.FeedView import build_interaction_map


class ArtistPostsView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(tags=['Artists'])
    def get(self, request, slug):
        artist = get_object_or_404(Artist, slug=slug)
        posts = list(
            Post.objects
            .filter(author__managed_artists=artist)
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