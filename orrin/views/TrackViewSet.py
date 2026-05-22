from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ..models import Track
from ..serializers import TrackSerializer


@extend_schema_view(
    list=extend_schema(tags=['Tracks']),
    retrieve=extend_schema(tags=['Tracks']),
    create=extend_schema(tags=['Tracks']),
    update=extend_schema(tags=['Tracks']),
    partial_update=extend_schema(tags=['Tracks']),
    destroy=extend_schema(tags=['Tracks']),
)
class TrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly]