import os
from django.contrib import admin
from mutagen import File
from .models import Track, Artist, BandMembership


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    fields = ('title', 'slug', 'artist', 'cover', 'audio', 'duration')
    autocomplete_fields = ['artist']
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


class BandMembershipInline(admin.TabularInline):
    model = BandMembership
    fk_name = 'group'
    extra = 1
    autocomplete_fields = ['member']
    verbose_name = "Member"
    verbose_name_plural = "Band Members"


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):

    fieldsets = (
        ('General Info', {
            'fields': ('name', 'slug', 'type', 'image', 'mini_description')
        }),
        ('Relations', {
            'fields': ('managers', 'genres'),
        }),
        ('Details', {
            'fields': ('about', 'history', 'location', 'join_date', 'monthly_listeners', 'socials'),
            'classes': ('collapse',),
        }),
    )

    list_display = ('name', 'type', 'is_solo_artist', 'slug')
    list_filter = ('type', 'genres')
    search_fields = ['name']
    readonly_fields = ('slug',)

    filter_horizontal = ('managers', 'genres')

    inlines = [BandMembershipInline]

    def is_solo_artist(self, obj):
        return obj.is_solo_artist

    is_solo_artist.boolean = True
    is_solo_artist.short_description = "Has Solo Tracks?"