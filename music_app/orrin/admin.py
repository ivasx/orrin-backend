from django.contrib import admin

from orrin.models import Track


# Register your models here.
@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    fields = ('title', 'slug', 'artist', 'cover', 'audio', 'duration')
    list_display = ('title', 'artist', 'cover', 'duration', 'slug')
    list_display_links = ('title',)
    readonly_fields = ('slug',)