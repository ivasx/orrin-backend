from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ..models import Artist
from ..serializers.ArtistSerializer import ArtistSerializer, ArtistDetailSerializer


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.prefetch_related('genres').all()
    serializer_class = ArtistSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'genres__name']
    ordering_fields = ['name', 'monthly_listeners']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ArtistDetailSerializer
        return ArtistSerializer

    def get_queryset(self):
        if self.action == 'retrieve':
            return (
                Artist.objects
                # 'followers' — reverse FK від FollowedArtist.artist
                # prefetch щоб get_followers_count і get_is_following не робили N+1
                .prefetch_related('genres', 'tracks', 'followers')
                .all()
            )
        return Artist.objects.prefetch_related('genres').all()