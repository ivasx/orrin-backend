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
        liked_entries = (
            LikedTrack.objects
            .filter(user=request.user)
            .select_related('track', 'track__artist')
            .order_by('-created_at')
        )

        liked_ids = {entry.track_id for entry in liked_entries}
        tracks = [entry.track for entry in liked_entries]

        serializer = LibraryTrackSerializer(
            tracks,
            many=True,
            context={'request': request, 'liked_ids': liked_ids},
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