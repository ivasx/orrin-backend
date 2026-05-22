from django.db.models import Count
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from feed.models import Post, PostLike, PostRepost, PostSave
from feed.serializers import PostSerializer, PostWriteSerializer

PAGE_SIZE = 10


def build_interaction_map(user, posts):
    if not user or not user.is_authenticated:
        return {'liked': set(), 'reposted': set(), 'saved': set()}
    post_ids = [p.id for p in posts]
    return {
        'liked':    set(PostLike.objects.filter(user=user,   post_id__in=post_ids).values_list('post_id', flat=True)),
        'reposted': set(PostRepost.objects.filter(user=user, post_id__in=post_ids).values_list('post_id', flat=True)),
        'saved':    set(PostSave.objects.filter(user=user,   post_id__in=post_ids).values_list('post_id', flat=True)),
    }


class FeedView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(tags=['Feed'])
    def get(self, request):
        feed_type    = request.query_params.get('feed_type', 'all')
        sort         = request.query_params.get('sort', 'recent')
        content_type = request.query_params.get('content_type')
        page         = max(int(request.query_params.get('page', 1)), 1)

        qs = Post.objects.select_related('author', 'track', 'track__artist')

        if feed_type == 'following' and request.user.is_authenticated:
            following_ids = request.user.following.values_list('id', flat=True)
            qs = qs.filter(author_id__in=following_ids)

        if content_type == 'with_music':
            qs = qs.filter(track__isnull=False)
        elif content_type == 'text_only':
            qs = qs.filter(track__isnull=True)

        if sort == 'popular':
            qs = qs.annotate(likes_total=Count('likes')).order_by('-likes_total', '-created_at')
        else:
            qs = qs.order_by('-created_at')

        total = qs.count()
        start = (page - 1) * PAGE_SIZE
        posts = list(qs[start:start + PAGE_SIZE])

        interaction_map = build_interaction_map(request.user, posts)
        serializer = PostSerializer(
            posts,
            many=True,
            context={'request': request, 'interaction_map': interaction_map},
        )

        return Response({
            'results': serializer.data,
            'count':   total,
            'next':    page + 1 if (start + PAGE_SIZE) < total else None,
        })

    @extend_schema(tags=['Feed'])
    def post(self, request):
        serializer = PostWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save(author=request.user)
        return Response(
            PostSerializer(post, context={'request': request}).data,
            status=status.HTTP_201_CREATED,
        )