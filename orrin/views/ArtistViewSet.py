from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ..models import Artist
from ..serializers import ArtistSerializer


@extend_schema_view(
    list=extend_schema(tags=['Artists']),
    retrieve=extend_schema(tags=['Artists']),
    create=extend_schema(tags=['Artists']),
    update=extend_schema(tags=['Artists']),
    partial_update=extend_schema(tags=['Artists']),
    destroy=extend_schema(tags=['Artists']),
)
class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly]