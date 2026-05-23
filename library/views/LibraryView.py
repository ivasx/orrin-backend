from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from library.models import LikedTrack, FollowedArtist
from library.serializers import LibraryTrackSerializer
from library.serializers.FollowedArtistSerializer import FollowedArtistSerializer
from orrin.models import PlaylistModel
from orrin.serializers import PlaylistSerializer


class LibraryView(APIView):
    """
    Aggregated endpoint: returns counts and first-page previews of
    liked tracks, followed artists and playlists in one request.
    Frontends that need full lists should call the individual endpoints.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        liked_entries = (
            LikedTrack.objects
            .filter(user=request.user)
            .select_related("track", "track__artist")
            .order_by("-created_at")
        )
        liked_ids = {e.track_id for e in liked_entries}
        tracks = [e.track for e in liked_entries[:10]]

        followed_entries = (
            FollowedArtist.objects
            .filter(user=request.user)
            .select_related("artist")
            .prefetch_related("artist__genres")
            .order_by("-created_at")
        )

        playlists = (
            PlaylistModel.objects
            .filter(owner=request.user)
            .prefetch_related("tracks")
            .order_by("-created_at")
        )

        return Response({
            "liked_tracks": {
                "count": liked_entries.count(),
                "results": LibraryTrackSerializer(
                    tracks,
                    many=True,
                    context={"request": request, "liked_ids": liked_ids},
                ).data,
            },
            "followed_artists": {
                "count": followed_entries.count(),
                "results": FollowedArtistSerializer(
                    followed_entries[:10],
                    many=True,
                    context={"request": request},
                ).data,
            },
            "playlists": {
                "count": playlists.count(),
                "results": PlaylistSerializer(
                    playlists[:10],
                    many=True,
                    context={"request": request},
                ).data,
            },
        })
