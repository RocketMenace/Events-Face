from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import SyncResultsModel


@admin.register(SyncResultsModel)
class SyncResultsAdmin(admin.ModelAdmin):
    list_display = (
        "created_at",
        "new_events_count",
        "updated_events_count",
        "last_synced_changed_at",
        "updated_at",
    )
    list_filter = ("created_at", "updated_at", "last_synced_changed_at")
    readonly_fields = ("id", "created_at", "updated_at")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"

    fieldsets = (
        (
            _("Basic Information"),
            {
                "fields": ("id",),
            },
        ),
        (
            _("Sync Statistics"),
            {
                "fields": (
                    "new_events_count",
                    "updated_events_count",
                    "last_synced_changed_at",
                ),
            },
        ),
        (
            _("Timestamps"),
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )
