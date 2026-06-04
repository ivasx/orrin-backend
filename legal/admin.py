from django.contrib import admin

from .models import LegalDocument


@admin.register(LegalDocument)
class LegalDocumentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'doc_type', 'language', 'title',
        'last_updated', 'is_active', 'updated_at',
    )
    list_display_links = ('id', 'title')
    list_filter = ('doc_type', 'language', 'is_active')
    search_fields = ('title',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('doc_type', 'language')

    fieldsets = (
        ('Document', {
            'fields': ('doc_type', 'language', 'title', 'last_updated', 'is_active'),
        }),
        ('Content', {
            'fields': ('sections',),
            'description': 'JSON array of { "id", "title", "content" } objects.',
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
