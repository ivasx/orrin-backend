from django.contrib import admin

from .models import LikedTrack, FollowedArtist, ListeningHistory, SavedAlbum


@admin.register(LikedTrack)
class LikedTrackAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'track', 'created_at')
    list_display_links = ('id',)
    list_filter = ('created_at',)
    search_fields = ('user__username', 'user__email', 'track__title', 'track__artist__name')
    readonly_fields = ('created_at',)
    raw_id_fields = ('user', 'track')
    ordering = ('-created_at',)


@admin.register(FollowedArtist)
class FollowedArtistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'artist', 'created_at')
    list_display_links = ('id',)
    list_filter = ('created_at',)
    search_fields = ('user__username', 'user__email', 'artist__name')
    readonly_fields = ('created_at',)
    raw_id_fields = ('user', 'artist')
    ordering = ('-created_at',)


@admin.register(ListeningHistory)
class ListeningHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'track', 'played_at')
    list_display_links = ('id',)
    list_filter = ('played_at',)
    search_fields = ('user__username', 'user__email', 'track__title', 'track__artist__name')
    readonly_fields = ('played_at',)
    raw_id_fields = ('user', 'track')
    ordering = ('-played_at',)


@admin.register(SavedAlbum)
class SavedAlbumAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'album', 'created_at')
    list_display_links = ('id',)
    list_filter = ('created_at',)
    search_fields = ('user__username', 'user__email', 'album__title', 'album__artist__name')
    readonly_fields = ('created_at',)
    raw_id_fields = ('user', 'album')
    ordering = ('-created_at',)
