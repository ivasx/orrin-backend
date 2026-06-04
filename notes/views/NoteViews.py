from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from notes.models import Note, NoteLike
from notes.serializers.NoteSerializer import NoteSerializer, NoteWriteSerializer


def _build_note_queryset(request, filters):
    """
    Return a visibility-aware queryset:
    - Public notes are always visible.
    - Private notes are visible only to their author.
    """
    qs = Note.objects.filter(**filters).select_related(
        'author', 'lyric_line'
    )
    user = request.user
    if user.is_authenticated:
        qs = qs.filter(Q(note_type='public') | Q(author=user))
    else:
        qs = qs.filter(note_type='public')
    return qs


def _liked_note_ids(user, notes):
    if not user.is_authenticated:
        return set()
    ids = [n.id for n in notes]
    return set(
        NoteLike.objects.filter(user=user, note_id__in=ids)
        .values_list('note_id', flat=True)
    )


class TrackNotesView(APIView):
    """GET /api/v1/tracks/<slug>/notes/   POST /api/v1/tracks/<slug>/notes/"""

    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(tags=['Notes'])
    def get(self, request, slug):
        notes = list(_build_note_queryset(request, {'track__slug': slug}))
        context = {
            'request': request,
            'liked_note_ids': _liked_note_ids(request.user, notes),
        }
        return Response(NoteSerializer(notes, many=True, context=context).data)

    @extend_schema(tags=['Notes'])
    def post(self, request, slug):
        data = {**request.data, 'track_slug': slug}
        serializer = NoteWriteSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        note = serializer.save(author=request.user)
        return Response(
            NoteSerializer(note, context={'request': request}).data,
            status=status.HTTP_201_CREATED,
        )


class ArtistNotesView(APIView):
    """GET /api/v1/artists/<slug>/notes/   POST /api/v1/artists/<slug>/notes/"""

    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(tags=['Notes'])
    def get(self, request, slug):
        notes = list(_build_note_queryset(request, {'artist__slug': slug}))
        context = {
            'request': request,
            'liked_note_ids': _liked_note_ids(request.user, notes),
        }
        return Response(NoteSerializer(notes, many=True, context=context).data)

    @extend_schema(tags=['Notes'])
    def post(self, request, slug):
        data = {**request.data, 'artist_slug': slug}
        serializer = NoteWriteSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        note = serializer.save(author=request.user)
        return Response(
            NoteSerializer(note, context={'request': request}).data,
            status=status.HTTP_201_CREATED,
        )


class NoteDetailView(APIView):
    """PATCH /api/v1/notes/<pk>/   DELETE /api/v1/notes/<pk>/"""

    permission_classes = [IsAuthenticated]

    def _get_own_note(self, request, pk):
        note = Note.objects.filter(pk=pk, author=request.user).first()
        if note is None:
            return None, Response(
                {'detail': 'Note not found or permission denied.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        return note, None

    @extend_schema(tags=['Notes'])
    def patch(self, request, pk):
        note, error = self._get_own_note(request, pk)
        if error:
            return error
        serializer = NoteWriteSerializer(note, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        note = serializer.save()
        return Response(NoteSerializer(note, context={'request': request}).data)

    @extend_schema(tags=['Notes'])
    def delete(self, request, pk):
        note, error = self._get_own_note(request, pk)
        if error:
            return error
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NoteLikeView(APIView):
    """POST /api/v1/notes/<pk>/like/"""

    permission_classes = [IsAuthenticated]

    @extend_schema(tags=['Notes'])
    def post(self, request, pk):
        note = Note.objects.filter(pk=pk, note_type='public').first()
        if note is None:
            return Response({'detail': 'Note not found.'}, status=status.HTTP_404_NOT_FOUND)

        like, created = NoteLike.objects.get_or_create(user=request.user, note=note)
        if not created:
            like.delete()
            return Response({'isLiked': False}, status=status.HTTP_200_OK)
        return Response({'isLiked': True}, status=status.HTTP_201_CREATED)
