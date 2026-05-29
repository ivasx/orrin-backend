from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html

from .models import User, Notification


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "id", "email", "username", "full_name", "avatar_preview",
        "followers_count", "following_count", "is_active", "is_staff", "date_joined",
    )
    list_display_links = ("id", "email")
    list_filter = ("is_active", "is_staff", "is_superuser", "gender", "date_joined")
    search_fields = ("email", "username", "first_name", "last_name")
    ordering = ("-date_joined",)
    readonly_fields = ("date_joined", "last_login", "avatar_preview", "cover_photo_preview")

    fieldsets = (
        ("Credentials", {"fields": ("email", "username", "password")}),
        ("Personal Info", {
            "fields": (
                "first_name", "last_name", "bio",
                "date_of_birth", "gender", "location", "website",
            ),
        }),
        ("Media", {"fields": ("avatar", "avatar_preview", "cover_photo", "cover_photo_preview")}),
        ("Social", {"fields": ("followers",)}),
        ("Permissions", {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions"),
            "classes": ("collapse",),
        }),
        ("Timestamps", {"fields": ("date_joined", "last_login"), "classes": ("collapse",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "password1", "password2"),
        }),
    )

    filter_horizontal = ("followers", "groups", "user_permissions")

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or "—"

    full_name.short_description = "Name"

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="40" height="40" style="border-radius:50%;object-fit:cover;">',
                               obj.avatar.url)
        return "—"

    avatar_preview.short_description = "Avatar"

    def cover_photo_preview(self, obj):
        if obj.cover_photo:
            return format_html('<img src="{}" width="200" height="60" style="object-fit:cover;">', obj.cover_photo.url)
        return "—"

    cover_photo_preview.short_description = "Cover"

    def followers_count(self, obj):
        return obj.followers.count()

    followers_count.short_description = "Followers"

    def following_count(self, obj):
        return obj.following.count()

    following_count.short_description = "Following"


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "notification_type", "actor", "recipient", "text_short", "is_read", "created_at")
    list_display_links = ("id",)
    list_filter = ("notification_type", "is_read", "created_at")
    search_fields = ("actor__username", "recipient__username", "text")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "content_type", "object_id")
    raw_id_fields = ("actor", "recipient")

    def text_short(self, obj):
        return obj.text[:60] + ("…" if len(obj.text) > 60 else "")

    text_short.short_description = "Text"
