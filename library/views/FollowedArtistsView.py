from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from orrin.models import Artist
from library.models import FollowedArtist
from library.serializers import FollowedArtistSerializer


class FollowedArtistsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=['Library'])
    def get(self, request):
        entries = (
            FollowedArtist.objects
            .filter(user=request.user)
            .select_related('artist')
        )
        serializer = FollowedArtistSerializer(
            entries,
            many=True,
            context={'request': request},
        )
        return Response(serializer.data)


class ArtistFollowToggleView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=['Artists'])
    def post(self, request, slug):
        artist = Artist.objects.filter(slug=slug).first()
        if artist is None:
            return Response(
                {'detail': 'Artist not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        follow, created = FollowedArtist.objects.get_or_create(
            user=request.user,
            artist=artist,
        )

        if not created:
            follow.delete()
            return Response({'is_following': False}, status=status.HTTP_200_OK)

        return Response({'is_following': True}, status=status.HTTP_201_CREATED)