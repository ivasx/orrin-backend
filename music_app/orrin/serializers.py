from django.template.context_processors import request
from rest_framework import serializers

from orrin.models import Track


class TrackSerializer(serializers.ModelSerializer):
    audio_url = serializers.SerializerMethodField()
    cover_url = serializers.SerializerMethodField()
    duration_formatted = serializers.CharField(read_only=True)
    trackId = serializers.CharField(source='slug', read_only=True)

    class Meta:
        model = Track
        fields = [
            'trackId',
            'slug',
            'title',
            'artist',
            # 'artistId',
            'duration',
            'duration_formatted',
            'cover_url',  # Поле для фронтенду
            'audio_url',  # Поле для фронтенду
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