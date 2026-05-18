from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from feed.models import Post, PostLike, PostRepost, PostSave, PostReport


class PostLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = Post.objects.filter(pk=pk).first()
        if post is None:
            return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

        like, created = PostLike.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
            return Response({'is_liked': False}, status=status.HTTP_200_OK)
        return Response({'is_liked': True}, status=status.HTTP_201_CREATED)


class PostRepostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = Post.objects.filter(pk=pk).first()
        if post is None:
            return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

        repost, created = PostRepost.objects.get_or_create(user=request.user, post=post)
        if not created:
            repost.delete()
            return Response({'is_reposted': False}, status=status.HTTP_200_OK)
        return Response({'is_reposted': True}, status=status.HTTP_201_CREATED)


class PostSaveView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = Post.objects.filter(pk=pk).first()
        if post is None:
            return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

        save, created = PostSave.objects.get_or_create(user=request.user, post=post)
        if not created:
            save.delete()
            return Response({'is_saved': False}, status=status.HTTP_200_OK)
        return Response({'is_saved': True}, status=status.HTTP_201_CREATED)


class PostReportView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = Post.objects.filter(pk=pk).first()
        if post is None:
            return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

        reason = request.data.get('reason', 'other')
        PostReport.objects.get_or_create(user=request.user, post=post, defaults={'reason': reason})
        return Response({'detail': 'Report submitted.'}, status=status.HTTP_200_OK)
