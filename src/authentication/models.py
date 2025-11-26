import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .manager import CustomUserManager


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255, verbose_name=_("username"), unique=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created_at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated_at"))

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.username}"

    objects = CustomUserManager()

    class Meta:
        db_table = _("users")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["email"], name="idx_user_email"),
            models.Index(fields=["is_active"], name="idx_user_is_active"),
        ]
        verbose_name = _("user")
        verbose_name_plural = _("users")
