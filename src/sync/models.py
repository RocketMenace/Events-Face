import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class SyncResults(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_("id"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("created_at"),
        db_index=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("updated_at"),
    )
    new_events_count = models.IntegerField(
        default=0,
        verbose_name=_("new_events_count"),
        help_text=_("Number of new events created during sync"),
    )
    updated_events_count = models.IntegerField(
        default=0,
        verbose_name=_("updated_events_count"),
        help_text=_("Number of events updated during sync"),
    )
    last_synced_changed_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_("last_synced_changed_at"),
        help_text=_("Date of the last synced event's changed_at field"),
        db_index=True,
    )

    class Meta:
        verbose_name = _("sync_result")
        verbose_name_plural = _("sync_results")
        db_table = "sync_results"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"], name="idx_sync_created_at"),
        ]

    def __str__(self) -> str:
        return f"Sync at {self.created_at} - New: {self.new_events_count}, Updated: {self.updated_events_count}"
