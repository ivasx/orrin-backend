from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model

from users.serializers import UserProfileSerializer

User = get_user_model()


@extend_schema(tags=['Users'])
class UserProfileDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]
    lookup_field = 'username'