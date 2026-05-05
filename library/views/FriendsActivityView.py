from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from library.models import ListeningHistory, LikedTrack
from library.serializers import LibraryTrackSerializer


class FriendsActivityView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        following_ids = request.user.following.values_list('id', flat=True)

        recent_entries = (
            ListeningHistory.objects
            .filter(user_id__in=following_ids)
            .select_related('track', 'track__artist')
            .order_by('-played_at')
            .distinct('track_id')[:20]
        )

        tracks = [entry.track for entry in recent_entries]

        liked_ids = set(
            LikedTrack.objects
            .filter(user=request.user, track__in=tracks)
            .values_list('track_id', flat=True)
        )

        serializer = LibraryTrackSerializer(
            tracks,
            many=True,
            context={'request': request, 'liked_ids': liked_ids},
        )
        return Response(serializer.data)
