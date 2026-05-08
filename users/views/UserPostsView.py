from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

User = get_user_model()


class UserPostsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, username):
        get_object_or_404(User, username=username)
        return Response([])
