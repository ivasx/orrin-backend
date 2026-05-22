from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import UserCompactSerializer

User = get_user_model()


class UserFollowersView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(tags=['Users'])
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        followers = user.followers.all()
        serializer = UserCompactSerializer(
            followers,
            many=True,
            context={'request': request},
        )
        return Response(serializer.data)


class UserFollowingView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(tags=['Users'])
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        following = user.following.all()
        serializer = UserCompactSerializer(
            following,
            many=True,
            context={'request': request},
        )
        return Response(serializer.data)