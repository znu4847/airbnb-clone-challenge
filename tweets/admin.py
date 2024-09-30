from django.contrib import admin
from .models import Tweet
from .models import Like


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ("payload", "user", "like_count", "created_at", "updated_at")
    list_filter = ("user",)
    search_fields = ("payload",)
    ordering = ("created_at",)
    list_per_page = 10
    list_max_show_all = 100
    list_select_related = ("user",)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("tweet", "user", "created_at", "updated_at")
    list_filter = ("user",)
    search_fields = ("tweet",)
    ordering = ("created_at",)
    list_per_page = 10
    list_max_show_all = 100
    list_select_related = ("user", "tweet")
