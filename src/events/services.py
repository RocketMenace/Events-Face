from .dto import EventAreaDTO, EventDTO
from .repository import EventAreaRepository, EventRepository


class EventsService:
    def __init__(self, repository: EventRepository):
        self.repository = repository

    def create_event(self, dto: EventDTO) -> EventDTO:
        return self.repository.create(dto=dto)

    def get_queryset(self, name_filter: str | None = None, order_by: str | None = None):
        return self.repository.get_queryset(name_filter=name_filter, order_by=order_by)

    def get_events(self, queryset=None) -> list[EventDTO]:
        return self.repository.get_list(queryset=queryset)


class AreaService:
    def __init__(self, repository: EventAreaRepository):
        self.repository = repository

    def create_area(self, dto: EventAreaDTO) -> EventAreaDTO:
        return self.repository.create(dto=dto)
