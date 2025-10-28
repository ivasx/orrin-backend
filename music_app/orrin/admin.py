import os

from django.contrib import admin
from mutagen import File

from orrin.models import Track


# Register your models here.
@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    fields = ('title', 'slug', 'artist', 'cover', 'audio', 'duration')
    list_display = ('title', 'artist', 'cover', 'duration', 'slug')
    list_display_links = ('title',)
    readonly_fields = ('slug', 'duration')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if obj.audio and os.path.exists(obj.audio.path):
            try:
                audio_file = File(obj.audio.path)
                if audio_file and audio_file.info:
                    obj.duration = int(audio_file.info.length)
                    obj.save(update_fields=['duration'])
            except Exception as e:
                print(f"Помилка при розрахунку тривалості: {e}")