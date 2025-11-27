from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import NotificationModel


@admin.register(NotificationModel)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("topic", "sent", "created_at", "sent_at")
    list_filter = ("sent", "topic", "created_at", "sent_at")
    search_fields = ("topic",)
    readonly_fields = ("id", "created_at", "sent_at")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"

    fieldsets = (
        (
            _("Basic Information"),
            {
                "fields": ("id", "topic", "payload"),
            },
        ),
        (
            _("Status"),
            {
                "fields": ("sent", "sent_at"),
            },
        ),
        (
            _("Timestamps"),
            {
                "fields": ("created_at",),
                "classes": ("collapse",),
            },
        ),
    )
