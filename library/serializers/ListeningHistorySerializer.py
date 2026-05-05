from rest_framework import serializers

from library.models import ListeningHistory
from library.serializers.LibraryTrackSerializer import LibraryTrackSerializer


class ListeningHistorySerializer(serializers.ModelSerializer):
    track = LibraryTrackSerializer(read_only=True)
    played_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = ListeningHistory
        fields = ['id', 'track', 'played_at']
