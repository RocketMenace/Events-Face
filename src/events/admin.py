from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import EventAreaModel, EventModel


@admin.register(EventAreaModel)
class EventAreaAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at", "event_count")
    list_filter = ("created_at", "updated_at")
    search_fields = ("name",)
    readonly_fields = ("id", "created_at", "updated_at")
    ordering = ("name",)
    date_hierarchy = "created_at"

    fieldsets = (
        (
            _("Basic Information"),
            {
                "fields": ("id", "name"),
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

    def event_count(self, obj):
        return obj.events.count()

    event_count.short_description = _("Number of Events")


class EventAreaInline(admin.TabularInline):
    model = EventModel
    extra = 0
    fields = ("name", "status", "event_datetime")
    readonly_fields = ("created_at", "updated_at")


@admin.register(EventModel)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "area",
        "status",
        "event_datetime",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", "area", "event_datetime", "created_at")
    search_fields = ("name", "area__name")
    readonly_fields = ("id", "created_at", "updated_at")
    ordering = ("-event_datetime", "name")
    date_hierarchy = "event_datetime"
    autocomplete_fields = ("area",)

    fieldsets = (
        (
            _("Basic Information"),
            {
                "fields": ("id", "name", "area"),
            },
        ),
        (
            _("Event Details"),
            {
                "fields": ("status", "event_datetime"),
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

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("area")
