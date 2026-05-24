from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import UserCompactSerializer

User = get_user_model()


class UserSearchView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(tags=['Users'])
    def get(self, request):
        query = request.query_params.get('search', '').strip()
        if not query:
            return Response([])

        users = (
            User.objects
            .filter(username__icontains=query)
            .exclude(is_active=False)
            .order_by('username')[:20]
        )

        serializer = UserCompactSerializer(users, many=True, context={'request': request})
        return Response(serializer.data)
