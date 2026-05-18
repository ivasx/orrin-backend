from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from feed.models import Post, PostComment
from feed.serializers import PostCommentSerializer


class PostCommentView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        post = Post.objects.filter(pk=pk).first()
        if post is None:
            return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

        comments = post.comments.select_related('author').order_by('-created_at')
        serializer = PostCommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, pk):
        post = Post.objects.filter(pk=pk).first()
        if post is None:
            return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

        text = request.data.get('text', '').strip()
        if not text:
            return Response({'detail': 'text is required.'}, status=status.HTTP_400_BAD_REQUEST)

        comment = PostComment.objects.create(post=post, author=request.user, text=text)
        serializer = PostCommentSerializer(comment, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
