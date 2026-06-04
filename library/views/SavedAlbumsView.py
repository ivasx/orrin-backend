from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from orrin.models import Album
from orrin.serializers import AlbumListSerializer
from library.models import SavedAlbum


class SavedAlbumsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=['Library'])
    def get(self, request):
        entries = (
            SavedAlbum.objects
            .filter(user=request.user)
            .select_related('album', 'album__artist')
            .order_by('-created_at')
        )
        albums = [entry.album for entry in entries]
        serializer = AlbumListSerializer(albums, many=True, context={'request': request})
        return Response(serializer.data)


class AlbumSaveToggleView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=['Library'])
    def post(self, request, slug):
        album = Album.objects.filter(slug=slug).first()
        if album is None:
            return Response(
                {'detail': 'Album not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        saved, created = SavedAlbum.objects.get_or_create(
            user=request.user,
            album=album,
        )
        if not created:
            saved.delete()
            return Response({'is_saved': False}, status=status.HTTP_200_OK)

        return Response({'is_saved': True}, status=status.HTTP_201_CREATED)
