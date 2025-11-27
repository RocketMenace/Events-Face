from typing import Protocol

from .dto import NotificationDTO
from .repository import NotificationsRepository


class NotificationsServiceProtocol(Protocol):
    def create_notification(self, dto: NotificationDTO) -> None: ...


class NotificationsService:
    def __init__(self, repository: NotificationsRepository):
        self.repository = repository

    def create_notification(self, dto: NotificationDTO) -> None:
        self.repository.create(dto=dto)
