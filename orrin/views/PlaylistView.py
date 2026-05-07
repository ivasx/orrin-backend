from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from orrin.models import PlaylistModel, Track, PlaylistTrack
from orrin.serializers import PlaylistSerializer, PlaylistDetailSerializer, PlaylistWriteSerializer


class PlaylistListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        playlists = (
            PlaylistModel.objects
            .filter(owner=request.user)
            .prefetch_related('tracks')
            .order_by('-created_at')
        )
        serializer = PlaylistSerializer(
            playlists,
            many=True,
            context={'request': request},
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = PlaylistWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        playlist = serializer.save(owner=request.user)
        return Response(
            PlaylistDetailSerializer(playlist, context={'request': request}).data,
            status=status.HTTP_201_CREATED,
        )


class PlaylistDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def _get_owned_playlist(self, request, pk):
        playlist = PlaylistModel.objects.filter(pk=pk).first()
        if playlist is None:
            return None, Response(
                {'detail': 'Playlist not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        if playlist.owner != request.user:
            return None, Response(
                {'detail': 'Permission denied.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        return playlist, None

    def get(self, request, pk):
        playlist = (
            PlaylistModel.objects
            .filter(pk=pk)
            .prefetch_related('tracks__artist')
            .first()
        )
        if playlist is None:
            return Response(
                {'detail': 'Playlist not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        if playlist.visibility == 'private' and playlist.owner != request.user:
            return Response(
                {'detail': 'Permission denied.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        return Response(
            PlaylistDetailSerializer(playlist, context={'request': request}).data
        )

    def patch(self, request, pk):
        playlist, error = self._get_owned_playlist(request, pk)
        if error:
            return error

        serializer = PlaylistWriteSerializer(playlist, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            PlaylistDetailSerializer(playlist, context={'request': request}).data
        )

    def delete(self, request, pk):
        playlist, error = self._get_owned_playlist(request, pk)
        if error:
            return error

        playlist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PlaylistTrackView(APIView):
    permission_classes = [IsAuthenticated]

    def _get_owned_playlist(self, request, pk):
        playlist = PlaylistModel.objects.filter(pk=pk, owner=request.user).first()
        if playlist is None:
            return None, Response(
                {'detail': 'Playlist not found or permission denied.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        return playlist, None

    def post(self, request, pk):
        playlist, error = self._get_owned_playlist(request, pk)
        if error:
            return error

        slug = request.data.get('track_slug')
        if not slug:
            return Response(
                {'detail': 'track_slug is required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        track = Track.objects.filter(slug=slug).first()
        if track is None:
            return Response(
                {'detail': 'Track not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        if PlaylistTrack.objects.filter(playlist=playlist, track=track).exists():
            return Response(
                {'detail': 'Track already in playlist.'},
                status=status.HTTP_409_CONFLICT,
            )

        next_order = PlaylistTrack.objects.filter(playlist=playlist).count()
        PlaylistTrack.objects.create(playlist=playlist, track=track, order=next_order)

        playlist.refresh_from_db()
        return Response(
            PlaylistDetailSerializer(playlist, context={'request': request}).data,
            status=status.HTTP_201_CREATED,
        )

    def delete(self, request, pk, track_slug):
        playlist, error = self._get_owned_playlist(request, pk)
        if error:
            return error

        track = Track.objects.filter(slug=track_slug).first()
        if track is None:
            return Response(
                {'detail': 'Track not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        deleted, _ = PlaylistTrack.objects.filter(
            playlist=playlist,
            track=track,
        ).delete()

        if not deleted:
            return Response(
                {'detail': 'Track not in playlist.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        self._reorder(playlist)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _reorder(self, playlist):
        entries = (
            PlaylistTrack.objects
            .filter(playlist=playlist)
            .order_by('order')
        )
        for i, entry in enumerate(entries):
            if entry.order != i:
                entry.order = i
                entry.save(update_fields=['order'])
