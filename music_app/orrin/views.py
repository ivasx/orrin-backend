import os

from django.conf import settings
from django.http import FileResponse
from django.views import View
from rest_framework import generics

from .models import Track
from .serializers import TrackSerializer


class TrackAPIView(generics.ListAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer


class TrackDetailAPIView(generics.RetrieveAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    lookup_field = 'slug'


class ServeAudioView(View):
    def get(self, request, path):
        file_path = os.path.join(settings.MEDIA_ROOT, 'audio', path)
        response = FileResponse(open(file_path, 'rb'))
        response['Accept-Ranges'] = 'bytes'
        return response