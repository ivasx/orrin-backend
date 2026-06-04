from django.contrib import admin

from .models import Note, NoteLike


class NoteLikeInline(admin.TabularInline):
    model = NoteLike
    extra = 0
    readonly_fields = ('user', 'created_at')
    fields = ('user', 'created_at')
    can_delete = True


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'author', 'note_type', 'track', 'artist',
        'timecode', 'likes_count', 'created_at',
    )
    list_display_links = ('id',)
    list_filter = ('note_type', 'created_at')
    search_fields = ('author__username', 'text', 'track__title', 'artist__name')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('author', 'track', 'artist', 'lyric_line')
    ordering = ('-created_at',)
    inlines = (NoteLikeInline,)

    fieldsets = (
        ('Note', {'fields': ('author', 'text', 'note_type')}),
        ('Context', {'fields': ('track', 'artist', 'timecode', 'lyric_line')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    def likes_count(self, obj):
        return obj.likes.count()
    likes_count.short_description = 'Likes'


@admin.register(NoteLike)
class NoteLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'note', 'created_at')
    list_display_links = ('id',)
    list_filter = ('created_at',)
    search_fields = ('user__username',)
    readonly_fields = ('created_at',)
    raw_id_fields = ('user', 'note')
    ordering = ('-created_at',)
