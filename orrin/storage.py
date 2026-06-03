import os

from cloudinary_storage.storage import MediaCloudinaryStorage

AUDIO_EXTENSIONS = {'.mp3', '.flac', '.wav', '.ogg', '.aac', '.m4a', '.opus'}


class SmartCloudinaryStorage(MediaCloudinaryStorage):
    """
    Routes files to the correct Cloudinary resource type based on file extension:
      - audio (.mp3, .flac, etc.) → resource_type=raw
      - everything else           → resource_type=image

    Plugged in via STORAGES["default"] — models stay storage-agnostic.
    """

    def _get_resource_type(self, name):
        ext = os.path.splitext(name or '')[1].lower()
        return 'raw' if ext in AUDIO_EXTENSIONS else 'image'