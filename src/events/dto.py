from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(kw_only=True)
class EventAreaDTO:
    name: str
    id: UUID | None = None


@dataclass(kw_only=True)
class EventDTO:
    name: str
    status: str
    event_datetime: datetime
    registration_deadline: datetime
    id: UUID | None = None
    area: str | None = None
    area_id: UUID | None = None
