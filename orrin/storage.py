import os

from django.core.files.storage import Storage


class SmartCloudinaryStorage(Storage):
    """
    Routes files to the correct Cloudinary resource type based on file extension.
    Images → MediaCloudinaryStorage (resource_type=image)
    Audio/raw files → RawMediaCloudinaryStorage (resource_type=raw)

    Plugged in via DEFAULT_FILE_STORAGE — models stay storage-agnostic.
    Swap the entire backend by replacing this class in settings.
    """

    AUDIO_EXTENSIONS = {'.mp3', '.flac', '.wav', '.ogg', '.aac', '.m4a', '.opus'}

    def _get_backend(self, name):
        from cloudinary_storage.storage import MediaCloudinaryStorage, RawMediaCloudinaryStorage
        ext = os.path.splitext(name)[1].lower()
        if ext in self.AUDIO_EXTENSIONS:
            return RawMediaCloudinaryStorage()
        return MediaCloudinaryStorage()

    def _open(self, name, mode='rb'):
        return self._get_backend(name)._open(name, mode)

    def _save(self, name, content):
        return self._get_backend(name)._save(name, content)

    def delete(self, name):
        return self._get_backend(name).delete(name)

    def exists(self, name):
        return self._get_backend(name).exists(name)

    def url(self, name):
        return self._get_backend(name).url(name)

    def size(self, name):
        return self._get_backend(name).size(name)

    def get_available_name(self, name, max_length=None):
        return self._get_backend(name).get_available_name(name, max_length=max_length)
