from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.services import notify_user

User = get_user_model()


class ToggleFollowView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        target = get_object_or_404(User, username=username)

        if target == request.user:
            return Response(
                {'detail': 'You cannot follow yourself.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        is_following = target.followers.filter(id=request.user.id).exists()

        if is_following:
            target.followers.remove(request.user)
            return Response({'is_following': False}, status=status.HTTP_200_OK)

        target.followers.add(request.user)
        notify_user(
            recipient=target,
            actor=request.user,
            notification_type='follow',
        )
        return Response({'is_following': True}, status=status.HTTP_200_OK)