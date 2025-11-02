from rest_framework import serializers
from ..models import Track

class TrackSerializer(serializers.ModelSerializer):
    audio_url = serializers.SerializerMethodField()
    cover_url = serializers.SerializerMethodField()
    duration_formatted = serializers.CharField(read_only=True)

    class Meta:
        model = Track
        fields = [
            'slug',
            'title',
            'artist',
            'duration',
            'duration_formatted',
            'cover_url',
            'audio_url',
        ]

    def get_audio_url(self, obj):
        request = self.context.get('request')
        if obj.audio and hasattr(obj.audio, 'url'):
            return request.build_absolute_uri(obj.audio.url)
        return None

    def get_cover_url(self, obj):
        request = self.context.get('request')
        if obj.cover and hasattr(obj.cover, 'url'):
            return request.build_absolute_uri(obj.cover.url)
        return None