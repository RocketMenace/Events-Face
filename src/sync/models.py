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
    new_measurements_count = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=_("new_measurements_count"),
        help_text=_("Number of new measurements created during sync"),
    )
    updated_measurements_count = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=_("updated_measurements_count"),
        help_text=_("Number of measurements updated during sync"),
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
        return f"Sync at {self.created_at} - New: {self.new_measurements_count or 0}, Updated: {self.updated_measurements_count or 0}"
