from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class SavedAlbumsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=['Library'])
    def get(self, request):
        return Response([])