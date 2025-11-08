import os

from django.conf import settings
from django.http import FileResponse
from django.views import View


class ServeAudioView(View):
    """
    Handles serving of audio files via an HTTP request.

    This class-based view is responsible for handling GET requests to serve audio
    files from the server's filesystem. It constructs a file path using the base
    media directory, appends the specific path passed in the request, and serves
    the requested audio file as a response. It enables the 'Accept-Ranges' header
    for byte serving, allowing efficient streaming and partial downloads of
    large audio files.
    """

    def get(self, request, path):
        file_path = os.path.join(settings.MEDIA_ROOT, 'audio', path)
        response = FileResponse(open(file_path, 'rb'))
        response['Accept-Ranges'] = 'bytes'
        return response