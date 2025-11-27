import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class NotificationModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_("id"),
    )
    topic = models.CharField(
        max_length=255,
        verbose_name=_("topic"),
        help_text=_("The topic/channel where the notification should be published"),
        null=False,
        blank=False,
        db_index=True,
    )
    payload = models.JSONField(
        verbose_name=_("payload"),
        help_text=_("The notification payload data"),
        null=False,
        blank=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("created_at"),
        db_index=True,
    )
    sent = models.BooleanField(
        default=False,
        verbose_name=_("sent"),
        help_text=_("Whether the notification has been sent"),
        db_index=True,
    )
    sent_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("sent_at"),
        help_text=_("Timestamp when the notification was sent"),
    )

    class Meta:
        verbose_name = _("notification")
        verbose_name_plural = _("notifications")
        db_table = "notifications"
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=["sent", "-created_at"],
                name="idx_notification_sent_created",
            ),
            models.Index(
                fields=["topic", "-created_at"],
                name="idx_notification_topic_created",
            ),
        ]

    def __str__(self) -> str:
        status = "sent" if self.sent else "pending"
        return f"{self.topic} - {status} ({self.created_at})"
