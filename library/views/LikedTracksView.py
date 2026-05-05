from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from orrin.models import Track
from library.models import LikedTrack
from library.serializers import LibraryTrackSerializer


class LikedTracksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        liked_track_ids = LikedTrack.objects.filter(
            user=request.user
        ).values_list('track_id', flat=True)

        tracks = (
            Track.objects
            .filter(id__in=liked_track_ids)
            .select_related('artist')
            .order_by('-liked_by__created_at')
        )

        serializer = LibraryTrackSerializer(
            tracks,
            many=True,
            context={'request': request, 'liked_ids': set(liked_track_ids)},
        )
        return Response(serializer.data)


class TrackLikeToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        track = Track.objects.filter(slug=slug).first()
        if track is None:
            return Response(
                {'detail': 'Track not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        liked, created = LikedTrack.objects.get_or_create(
            user=request.user,
            track=track,
        )

        if not created:
            liked.delete()
            return Response({'is_liked': False}, status=status.HTTP_200_OK)

        return Response({'is_liked': True}, status=status.HTTP_201_CREATED)
