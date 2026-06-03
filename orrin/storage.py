import os
import logging

from cloudinary_storage.storage import MediaCloudinaryStorage

logger = logging.getLogger(__name__)

AUDIO_EXTENSIONS = {'.mp3', '.flac', '.wav', '.ogg', '.aac', '.m4a', '.opus'}


class SmartCloudinaryStorage(MediaCloudinaryStorage):

    def _get_resource_type(self, name):
        ext = os.path.splitext(name or '')[1].lower()
        resource_type = 'raw' if ext in AUDIO_EXTENSIONS else 'image'
        logger.warning(f"[STORAGE] _get_resource_type: name={name} ext={ext} → {resource_type}")
        return resource_type

    def _save(self, name, content):
        logger.warning(f"[STORAGE] _save START: name={name}")
        try:
            result = super()._save(name, content)
            logger.warning(f"[STORAGE] _save SUCCESS: result={result}")
            return result
        except Exception as e:
            logger.warning(f"[STORAGE] _save ERROR: {e}", exc_info=True)
            raise

    def url(self, name):
        result = super().url(name)
        logger.warning(f"[STORAGE] url: name={name} → {result}")
        return result