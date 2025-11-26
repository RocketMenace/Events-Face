from django.utils.translation import gettext_lazy as _

from ..common.exceptions import BaseServiceException


class InvalidPassword(BaseServiceException):
    default_detail = _("Invalid password")


class AuthenticationError(BaseServiceException):
    default_detail = _("Invalid credentials")


class InvalidToken(BaseServiceException):
    default_detail = _("Invalid token")


class UserNotFound(BaseServiceException):
    default_detail = _("User with this username not found")
    default_code = "error"


class UserAlreadyExists(BaseServiceException):
    default_detail = _("User with this username already exists")
    default_code = "error"
