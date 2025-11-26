import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


# TODO: write validators for admin panel
class EventAreaModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_("id"),
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_("name"),
        help_text=_("The name of the event area"),
        null=False,
        blank=False,
        unique=True,
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

    class Meta:
        verbose_name = _("event_area")
        verbose_name_plural = _("event_areas")
        db_table = "event_areas"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"], name="idx_name"),
            models.Index(fields=["-created_at"], name="idx_area_created_at"),
        ]

    def __str__(self) -> str:
        return f"{self.name}"


class EventModel(models.Model):
    class EventStatus(models.TextChoices):
        OPEN = "open", _("Open")
        CLOSED = "closed", _("Closed")

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_("id"),
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_("name"),
        help_text=_("The name of the event"),
        null=False,
        blank=False,
    )
    registration_deadline = models.DateTimeField(
        verbose_name=_("registration_deadline"),
        db_index=True,
    )
    area = models.ForeignKey(
        to=EventAreaModel,
        related_name="events",
        on_delete=models.CASCADE,
        verbose_name=_("area"),
        db_index=True,
        blank=True,
        null=True,
    )
    status = models.CharField(
        max_length=10,
        choices=EventStatus.choices,
        default=EventStatus.OPEN,
        verbose_name=_("status"),
        db_index=True,
        help_text=_("Current status of the event"),
        null=False,
        blank=False,
    )
    event_datetime = models.DateTimeField(
        verbose_name=_("event_datetime"),
        help_text=_("Date and time when the event takes place"),
        db_index=True,
        null=False,
        blank=False,
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

    class Meta:
        verbose_name = _("event")
        verbose_name_plural = _("events")
        db_table = "events"
        ordering = ["-event_datetime", "name"]
        indexes = [
            models.Index(
                fields=["status", "-event_datetime"],
                name="idx_status_datetime",
            ),
            models.Index(fields=["area", "-event_datetime"], name="idx_area_datetime"),
            models.Index(fields=["-created_at"], name="idx_event_created_at"),
        ]

    def __str__(self) -> str:
        return f"{self.name} {self.event_datetime}"
