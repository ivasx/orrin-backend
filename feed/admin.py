from django.contrib import admin

from .models import Post, PostComment, PostLike, PostRepost, PostSave, PostReport


class PostCommentInline(admin.TabularInline):
    model = PostComment
    extra = 0
    readonly_fields = ("author", "text", "created_at")
    fields = ("author", "text", "created_at")
    show_change_link = True
    can_delete = True


class PostLikeInline(admin.TabularInline):
    model = PostLike
    extra = 0
    readonly_fields = ("user", "created_at")
    fields = ("user", "created_at")
    can_delete = True


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "text_short", "track", "likes_count", "reposts_count", "comments_count", "created_at")
    list_display_links = ("id",)
    list_filter = ("created_at",)
    search_fields = ("author__username", "author__email", "text")
    readonly_fields = ("created_at", "updated_at")
    raw_id_fields = ("author", "track")
    ordering = ("-created_at",)
    inlines = (PostCommentInline, PostLikeInline)

    fieldsets = (
        ("Post", {"fields": ("author", "text", "track")}),
        ("Timestamps", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def text_short(self, obj):
        return obj.text[:80] + ("…" if len(obj.text) > 80 else "")
    text_short.short_description = "Text"

    def likes_count(self, obj):
        return obj.likes.count()
    likes_count.short_description = "Likes"

    def reposts_count(self, obj):
        return obj.reposts.count()
    reposts_count.short_description = "Reposts"

    def comments_count(self, obj):
        return obj.comments.count()
    comments_count.short_description = "Comments"


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "post", "text_short", "created_at")
    list_display_links = ("id",)
    list_filter = ("created_at",)
    search_fields = ("author__username", "text")
    readonly_fields = ("created_at",)
    raw_id_fields = ("author", "post")
    ordering = ("-created_at",)

    def text_short(self, obj):
        return obj.text[:80] + ("…" if len(obj.text) > 80 else "")
    text_short.short_description = "Text"


@admin.register(PostReport)
class PostReportAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "post", "reason", "created_at")
    list_display_links = ("id",)
    list_filter = ("reason", "created_at")
    search_fields = ("user__username", "post__id")
    readonly_fields = ("created_at",)
    raw_id_fields = ("user", "post")
    ordering = ("-created_at",)