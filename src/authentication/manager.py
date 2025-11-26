from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(
        self,
        username: str,
        password: str = None,
        **extra_fields,
    ):
        user = self.model(
            username=username,
            password=password,
            **extra_fields,
        )
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        username: str,
        password: str,
        **extra_fields,
    ):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff"):
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser"):
            raise ValueError(_("Superuser must have is_superuser=True."))
        user = self.create_user(
            username=username,
            password=password,
            **extra_fields,
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user
