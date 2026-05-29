from django.contrib import admin

from .models import Chat, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ("sender", "text", "track_id", "is_read", "created_at")
    fields = ("sender", "text", "track_id", "is_read", "created_at")
    ordering = ("created_at",)
    can_delete = True
    show_change_link = True


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ("id", "participant_list", "message_count", "unread_count", "created_at", "updated_at")
    list_display_links = ("id",)
    list_filter = ("created_at",)
    search_fields = ("participants__username", "participants__email")
    readonly_fields = ("created_at", "updated_at")
    filter_horizontal = ("participants",)
    ordering = ("-updated_at",)
    inlines = (MessageInline,)

    def participant_list(self, obj):
        return ", ".join(obj.participants.values_list("username", flat=True))
    participant_list.short_description = "Participants"

    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = "Messages"

    def unread_count(self, obj):
        return obj.messages.filter(is_read=False).count()
    unread_count.short_description = "Unread"


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "chat", "sender", "text_short", "track_id", "is_read", "created_at")
    list_display_links = ("id",)
    list_filter = ("is_read", "created_at")
    search_fields = ("sender__username", "text")
    readonly_fields = ("created_at",)
    raw_id_fields = ("chat", "sender")
    ordering = ("-created_at",)

    def text_short(self, obj):
        return obj.text[:80] + ("…" if len(obj.text) > 80 else "")
    text_short.short_description = "Text"