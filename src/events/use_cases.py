from .dto import EventAreaDTO, EventDTO
from .serializers import EventAreaResponseSerializer, EventResponseSerializer
from .services import AreaService, EventsService


class GetEventsUseCase:
    def __init__(self, service: EventsService):
        self.service = service

    def get_queryset(self, name_filter: str | None = None, order_by: str | None = None):
        return self.service.get_queryset(name_filter=name_filter, order_by=order_by)

    def execute(self, queryset=None) -> EventResponseSerializer:
        events = self.service.get_events(queryset=queryset)
        serializer = EventResponseSerializer.from_dtos(dtos=events)
        return serializer


class CreateEventUseCase:
    def __init__(self, service: EventsService):
        self.service = service

    def execute(self, dto: EventDTO) -> EventResponseSerializer:
        event = self.service.create_event(dto=dto)
        return EventResponseSerializer.from_dto(dto=event)


class CreateAreaUseCase:
    def __init__(self, service: AreaService):
        self.service = service

    def execute(self, dto: EventAreaDTO) -> EventAreaResponseSerializer:
        area = self.service.create_area(dto=dto)
        return EventAreaResponseSerializer.from_dto(dto=area)
