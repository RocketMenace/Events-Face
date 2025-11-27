from django.utils.translation import gettext_lazy as _

from ..common.exceptions import BaseServiceException


class EventClosedError(BaseServiceException):
    default_detail = _("Event is closed")


class DuplicateRegistrationError(BaseServiceException):
    default_detail = _("Registration already exists")
