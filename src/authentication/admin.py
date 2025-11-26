from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "is_superuser",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "is_staff",
        "is_active",
        "is_superuser",
        "created_at",
        "updated_at",
    )
    search_fields = ("username", "email", "first_name", "last_name")
    readonly_fields = ("id", "created_at", "updated_at", "date_joined", "last_login")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                ),
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            _("Important dates"),
            {
                "fields": (
                    "id",
                    "created_at",
                    "updated_at",
                    "last_login",
                    "date_joined",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "email",
                    "first_name",
                    "last_name",
                ),
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )

    filter_horizontal = ("groups", "user_permissions")
