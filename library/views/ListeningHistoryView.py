from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from orrin.models import Track
from library.models import ListeningHistory
from library.serializers import ListeningHistorySerializer


class ListeningHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        entries = (
            ListeningHistory.objects
            .filter(user=request.user)
            .select_related('track', 'track__artist')
        )
        serializer = ListeningHistorySerializer(
            entries,
            many=True,
            context={'request': request},
        )
        return Response(serializer.data)

    def post(self, request):
        slug = request.data.get('track_slug')
        if not slug:
            return Response(
                {'detail': 'track_slug is required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        track = Track.objects.filter(slug=slug).select_related('artist').first()
        if track is None:
            return Response(
                {'detail': 'Track not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        entry = ListeningHistory.objects.create(user=request.user, track=track)
        serializer = ListeningHistorySerializer(entry, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        ListeningHistory.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListeningHistoryEntryView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        entry = get_object_or_404(ListeningHistory, pk=pk, user=request.user)
        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
