from django.contrib import admin
from .models import Tweet
from .models import Like


class TheGuyFilter(admin.SimpleListFilter):
    title = "You-Know-Who"
    parameter_name = "the_guy"

    def lookups(self, request, model_admin):
        return (
            ("show", "show"),
            ("hide", "hide"),
        )

    def queryset(self, request, queryset):
        if self.value() == "hide":
            return queryset.exclude(payload__icontains="Elon Musk")
        return queryset

    # hide 'All' option
    def choices(self, changelist):
        yield {
            "selected": self.value() is None,
            "query_string": changelist.get_query_string(remove=[self.parameter_name]),
            # "display": _("All"),
        }
        for lookup, title in self.lookup_choices:
            yield {
                "selected": self.value() == str(lookup),
                "query_string": changelist.get_query_string(
                    {self.parameter_name: lookup}
                ),
                "display": title,
            }


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ("payload", "user", "like_count", "created_at", "updated_at")
    list_filter = ("created_at", TheGuyFilter)
    search_fields = ("payload", "user__username")
    ordering = ("created_at",)
    list_per_page = 10
    list_max_show_all = 100


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("tweet_message", "tweet_author", "user", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username",)
    ordering = ("created_at",)
    list_per_page = 10
    list_max_show_all = 100
