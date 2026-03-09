from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from users.services import notify_user

User = get_user_model()


class ToggleFollowView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        target_user = get_object_or_404(User, username=username)

        if target_user == request.user:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )

        is_following = target_user.followers.filter(id=request.user.id).exists()

        if is_following:
            target_user.followers.remove(request.user)
            return Response({"status": "unfollowed", "is_following": False}, status=status.HTTP_200_OK)
        else:
            target_user.followers.add(request.user)

            notify_user(
                recipient=target_user,
                actor=request.user,
                notification_type='follow'
            )

            return Response({"status": "followed", "is_following": True}, status=status.HTTP_200_OK)