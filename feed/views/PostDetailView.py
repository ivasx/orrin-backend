from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from feed.models import Post
from feed.serializers import PostSerializer, PostWriteSerializer


class PostDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def _get_post(self, pk):
        return Post.objects.filter(pk=pk).select_related('author', 'track', 'track__artist').first()

    def get(self, request, pk):
        post = self._get_post(pk)
        if post is None:
            return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(PostSerializer(post, context={'request': request}).data)

    def patch(self, request, pk):
        post = self._get_post(pk)
        if post is None:
            return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)
        if post.author != request.user:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = PostWriteSerializer(post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        post = serializer.save()
        return Response(PostSerializer(post, context={'request': request}).data)

    def delete(self, request, pk):
        post = self._get_post(pk)
        if post is None:
            return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)
        if post.author != request.user:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
