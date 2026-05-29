from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class EmailOrUsernameTokenSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)


@extend_schema(tags=['Auth'])
class EmailOrUsernameTokenObtainPairView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = EmailOrUsernameTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        login_field = serializer.validated_data['username']
        password = serializer.validated_data['password']

        from django.contrib.auth import authenticate
        user = authenticate(request, username=login_field, password=password)

        if user is None:
            return Response(
                {'detail': 'No active account found with the given credentials.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
