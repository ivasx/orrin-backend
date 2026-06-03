import os

from cloudinary_storage.storage import MediaCloudinaryStorage

AUDIO_EXTENSIONS = {'.mp3', '.flac', '.wav', '.ogg', '.aac', '.m4a', '.opus'}


class SmartCloudinaryStorage(MediaCloudinaryStorage):
    """
    Single Cloudinary storage class that automatically routes files
    to the correct resource_type based on file extension:
      - audio files (.mp3, .flac, etc.) → resource_type=raw
      - everything else (images)        → resource_type=image

    Plugged in via DEFAULT_FILE_STORAGE — models stay storage-agnostic.
    To switch from Cloudinary to S3, replace only DEFAULT_FILE_STORAGE in production.py.
    """

    def _get_resource_type(self, name):
        ext = os.path.splitext(name or '')[1].lower()
        if ext in AUDIO_EXTENSIONS:
            return 'raw'
        return 'image'
