from django.db.models import Count
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from library.models import ListeningHistory
from orrin.models import Track, Artist
from orrin.serializers import TrackSerializer, ArtistSerializer


def _preserve_order(model_cls, pk_list, **select_related_fields):
    qs = model_cls.objects.filter(id__in=pk_list)
    if select_related_fields:
        qs = qs.select_related(*select_related_fields)
    obj_map = {obj.id: obj for obj in qs}
    return [obj_map[pk] for pk in pk_list if pk in obj_map]


class TopTracksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        limit = min(int(request.query_params.get('limit', 10)), 50)

        track_ids = list(
            ListeningHistory.objects
            .filter(user=request.user)
            .values('track_id')
            .annotate(play_count=Count('id'))
            .order_by('-play_count')
            .values_list('track_id', flat=True)[:limit]
        )

        tracks = _preserve_order(Track, track_ids, 'artist')
        return Response(TrackSerializer(tracks, many=True, context={'request': request}).data)


class TopArtistsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        limit = min(int(request.query_params.get('limit', 10)), 50)

        artist_ids = list(
            ListeningHistory.objects
            .filter(user=request.user)
            .values('track__artist_id')
            .annotate(play_count=Count('id'))
            .order_by('-play_count')
            .values_list('track__artist_id', flat=True)[:limit]
        )

        artists = _preserve_order(Artist, artist_ids)
        return Response(ArtistSerializer(artists, many=True, context={'request': request}).data)


class TopAlbumsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        limit = min(int(request.query_params.get('limit', 10)), 50)

        track_ids = list(
            ListeningHistory.objects
            .filter(user=request.user)
            .values('track_id')
            .annotate(play_count=Count('id'))
            .order_by('-play_count')
            .values_list('track_id', flat=True)[:limit]
        )

        tracks = _preserve_order(Track, track_ids, 'artist')
        return Response(TrackSerializer(tracks, many=True, context={'request': request}).data)
