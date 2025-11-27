from uuid import UUID

from django.db import transaction

from ..notifications.dto import NotificationDTO
from ..notifications.services import NotificationsServiceProtocol
from ..notifications.utils import generate_code
from .dto import EventAreaDTO, EventDTO, VisitorDTO
from .exceptions import DuplicateRegistrationError, EventClosedError
from .repository import EventAreaRepository, EventRepository, VisitorRepository


class EventsService:
    def __init__(self, repository: EventRepository):
        self.repository = repository

    def create_event(self, dto: EventDTO) -> EventDTO:
        return self.repository.create(dto=dto)

    def get_queryset(self, name_filter: str | None = None, order_by: str | None = None):
        return self.repository.get_queryset(name_filter=name_filter, order_by=order_by)

    def get_events(self, queryset=None) -> list[EventDTO]:
        return self.repository.get_list(queryset=queryset)

    def check_event_status(self, event_id: UUID) -> bool:
        return self.repository.get_open_events(event_id=event_id)


class AreaService:
    def __init__(self, repository: EventAreaRepository):
        self.repository = repository

    def create_area(self, dto: EventAreaDTO) -> EventAreaDTO:
        return self.repository.create(dto=dto)


class VisitorService:
    def __init__(self, repository: VisitorRepository):
        self.repository = repository

    def sign_in(self, dto: VisitorDTO) -> VisitorDTO:
        return self.repository.create(dto=dto)

    def check_visitor_registration(self, dto: VisitorDTO) -> bool:
        return self.repository.is_visitor_registered(dto=dto)


class OutboxService:
    def __init__(
        self,
        visitor_service: VisitorService,
        notifications_service: NotificationsServiceProtocol,
        events_service: EventsService,
    ):
        self.visitor_service = visitor_service
        self.notifications_service = notifications_service
        self.events_service = events_service

    def register_visitor(self, visitor_dto: VisitorDTO) -> None:
        with transaction.atomic():
            if not self.events_service.check_event_status(
                event_id=visitor_dto.event_id,
            ):
                raise EventClosedError
            if self.visitor_service.check_visitor_registration(dto=visitor_dto):
                raise DuplicateRegistrationError
            code = generate_code()
            visitor = self.visitor_service.sign_in(dto=visitor_dto)
            notification_dto = NotificationDTO(
                topic="event_signing",
                payload={
                    "owner_id": str(visitor.id),
                    "email": visitor.email,
                    "message": f"{code}",
                },
            )
            self.notifications_service.create_notification(dto=notification_dto)
