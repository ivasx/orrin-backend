import os

from django.contrib import admin
from django.utils.html import format_html
from mutagen import File

from .models import (
    Track,
    Artist,
    BandMembership,
    Genre,
    PlaylistModel,
    PlaylistTrack,
    Album,
    AlbumTrack,
    Lyrics,
    LyricLine,
)



@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'artist_count')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)

    def artist_count(self, obj):
        return obj.artists.count()
    artist_count.short_description = 'Artists'



class BandMembershipInline(admin.TabularInline):
    model = BandMembership
    fk_name = 'group'
    extra = 1
    autocomplete_fields = ('member',)
    verbose_name = 'Member'
    verbose_name_plural = 'Band Members'
    fields = ('member', 'role', 'join_date', 'leave_date')


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'image_preview', 'name', 'type', 'slug',
        'genre_list', 'monthly_listeners', 'is_verified',
        'track_count', 'follower_count',
    )
    list_display_links = ('id', 'name')
    list_filter = ('type', 'genres', 'is_verified')
    search_fields = ('name',)
    readonly_fields = ('slug', 'image_preview')
    ordering = ('name',)
    filter_horizontal = ('managers', 'genres')
    inlines = (BandMembershipInline,)

    fieldsets = (
        ('General', {
            'fields': (
                'name', 'slug', 'type', 'image', 'image_preview',
                'mini_description', 'is_verified',
            ),
        }),
        ('Relations', {'fields': ('managers', 'genres')}),
        ('Details', {
            'fields': ('about', 'history', 'location', 'join_date', 'monthly_listeners', 'socials'),
            'classes': ('collapse',),
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="40" height="40" style="object-fit:cover;border-radius:4px;">',
                obj.image.url,
            )
        return '—'
    image_preview.short_description = 'Photo'

    def genre_list(self, obj):
        return ', '.join(obj.genres.values_list('name', flat=True)) or '—'
    genre_list.short_description = 'Genres'

    def track_count(self, obj):
        return obj.tracks.count()
    track_count.short_description = 'Tracks'

    def follower_count(self, obj):
        return obj.followers.count()
    follower_count.short_description = 'Followers'



class LyricLineInline(admin.TabularInline):
    model = LyricLine
    fk_name = 'lyrics'
    extra = 3
    fields = ('time_seconds', 'text')
    ordering = ('time_seconds',)
    verbose_name = 'Lyric line'
    verbose_name_plural = 'Lyric lines'


class LyricsInline(admin.StackedInline):
    model = Lyrics
    extra = 0
    max_num = 1
    fields = ('lyrics_type', 'plain_text')
    verbose_name = 'Lyrics'
    verbose_name_plural = 'Lyrics'
    show_change_link = True


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'cover_preview', 'title', 'artist',
        'duration_display', 'plays_count', 'slug', 'playlist_count',
    )
    list_display_links = ('id', 'title')
    list_filter = ('artist',)
    search_fields = ('title', 'artist__name')
    autocomplete_fields = ('artist',)
    readonly_fields = ('slug', 'duration', 'plays_count', 'cover_preview')
    ordering = ('-id',)
    inlines = (LyricsInline,)

    fieldsets = (
        ('Track Info', {'fields': ('title', 'slug', 'artist')}),
        ('Media', {'fields': ('cover', 'cover_preview', 'audio', 'duration')}),
        ('Stats', {'fields': ('plays_count',)}),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.audio and os.path.exists(obj.audio.path):
            try:
                audio_file = File(obj.audio.path)
                if audio_file and audio_file.info:
                    obj.duration = int(audio_file.info.length)
                    obj.save(update_fields=('duration',))
            except Exception:
                pass

    def cover_preview(self, obj):
        if obj.cover:
            return format_html(
                '<img src="{}" width="40" height="40" style="object-fit:cover;border-radius:4px;">',
                obj.cover.url,
            )
        return '—'
    cover_preview.short_description = 'Cover'

    def duration_display(self, obj):
        return obj.duration_formatted()
    duration_display.short_description = 'Duration'

    def playlist_count(self, obj):
        return obj.in_playlists.count()
    playlist_count.short_description = 'In Playlists'



@admin.register(Lyrics)
class LyricsAdmin(admin.ModelAdmin):
    list_display = ('id', 'track', 'lyrics_type', 'line_count')
    list_display_links = ('id', 'track')
    list_filter = ('lyrics_type',)
    search_fields = ('track__title', 'track__artist__name')
    raw_id_fields = ('track',)
    inlines = (LyricLineInline,)

    def line_count(self, obj):
        return obj.lines.count()
    line_count.short_description = 'Lines'



class AlbumTrackInline(admin.TabularInline):
    model = AlbumTrack
    extra = 1
    autocomplete_fields = ('track',)
    fields = ('track_number', 'track')
    ordering = ('track_number',)
    verbose_name = 'Track'
    verbose_name_plural = 'Tracks'


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'cover_preview', 'title', 'artist',
        'album_type', 'year', 'track_count',
    )
    list_display_links = ('id', 'title')
    list_filter = ('album_type', 'year', 'artist')
    search_fields = ('title', 'artist__name')
    autocomplete_fields = ('artist',)
    readonly_fields = ('slug', 'cover_preview')
    ordering = ('-year', 'title')
    inlines = (AlbumTrackInline,)

    fieldsets = (
        ('Album Info', {'fields': ('title', 'slug', 'artist', 'album_type', 'year')}),
        ('Cover', {'fields': ('cover', 'cover_preview')}),
    )

    def cover_preview(self, obj):
        if obj.cover:
            return format_html(
                '<img src="{}" width="40" height="40" style="object-fit:cover;border-radius:4px;">',
                obj.cover.url,
            )
        return '—'
    cover_preview.short_description = 'Cover'

    def track_count(self, obj):
        return obj.tracks.count()
    track_count.short_description = 'Tracks'


class PlaylistTrackInline(admin.TabularInline):
    model = PlaylistTrack
    extra = 0
    autocomplete_fields = ('track',)
    fields = ('order', 'track', 'added_date')
    readonly_fields = ('added_date',)
    ordering = ('order',)


@admin.register(PlaylistModel)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'cover_preview', 'title', 'owner',
        'visibility', 'track_count', 'created_at',
    )
    list_display_links = ('id', 'title')
    list_filter = ('visibility', 'created_at')
    search_fields = ('title', 'owner__username', 'owner__email')
    readonly_fields = ('slug', 'cover_preview', 'created_at')
    raw_id_fields = ('owner',)
    inlines = (PlaylistTrackInline,)

    fieldsets = (
        ('Playlist', {'fields': ('title', 'slug', 'description', 'owner', 'visibility')}),
        ('Cover', {'fields': ('cover', 'cover_preview')}),
        ('Timestamps', {'fields': ('created_at',), 'classes': ('collapse',)}),
    )

    def cover_preview(self, obj):
        if obj.cover:
            return format_html(
                '<img src="{}" width="40" height="40" style="object-fit:cover;border-radius:4px;">',
                obj.cover.url,
            )
        return '—'
    cover_preview.short_description = 'Cover'

    def track_count(self, obj):
        return obj.tracks.count()
    track_count.short_description = 'Tracks'
