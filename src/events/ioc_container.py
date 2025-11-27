from functools import lru_cache

import punq

from ..notifications.repository import NotificationsRepository
from ..notifications.services import NotificationsService, NotificationsServiceProtocol
from .repository import EventAreaRepository, EventRepository, VisitorRepository
from .services import AreaService, EventsService, OutboxService, VisitorService
from .use_cases import (
    CreateAreaUseCase,
    CreateEventUseCase,
    GetEventsUseCase,
    SignUpForEventUseCase,
)


def _initialize_container() -> punq.Container:
    container = punq.Container()

    container.register(EventRepository, EventRepository)
    container.register(EventAreaRepository, EventAreaRepository)
    container.register(VisitorRepository, VisitorRepository)
    container.register(NotificationsRepository, NotificationsRepository)

    container.register(EventsService, EventsService)
    container.register(AreaService, AreaService)
    container.register(NotificationsServiceProtocol, NotificationsService)
    container.register(OutboxService, OutboxService)
    container.register(VisitorService)

    container.register(GetEventsUseCase, GetEventsUseCase)
    container.register(CreateAreaUseCase, CreateAreaUseCase)
    container.register(CreateEventUseCase, CreateEventUseCase)
    container.register(SignUpForEventUseCase, SignUpForEventUseCase)

    return container


@lru_cache
def get_container() -> punq.Container:
    return _initialize_container()
