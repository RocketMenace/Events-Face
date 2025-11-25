from functools import lru_cache

import punq

from .repository import EventAreaRepository, EventRepository
from .services import AreaService, EventsService
from .use_cases import CreateAreaUseCase, CreateEventUseCase, GetEventsUseCase


def _initialize_container() -> punq.Container:
    container = punq.Container()

    container.register(EventRepository, EventRepository)
    container.register(EventAreaRepository, EventAreaRepository)

    container.register(EventsService, EventsService)
    container.register(AreaService, AreaService)

    container.register(GetEventsUseCase, GetEventsUseCase)
    container.register(CreateAreaUseCase, CreateAreaUseCase)
    container.register(CreateEventUseCase, CreateEventUseCase)

    return container


@lru_cache
def get_container() -> punq.Container:
    return _initialize_container()
