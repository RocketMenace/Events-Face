from django.core.exceptions import ValidationError

from .dto import EventAreaDTO, EventDTO
from .models import EventAreaModel, EventModel


class EventRepository:
    model = EventModel

    def create(self, dto: EventDTO) -> EventDTO:
        try:
            obj = self.model(
                name=dto.name,
                status=dto.status,
                area_id=dto.area_id,
                event_datetime=dto.event_datetime,
            )
            obj.full_clean()
            obj.save()
            return EventDTO(
                id=obj.id,
                name=obj.name,
                status=obj.status,
                area_id=obj.area_id,
                area=obj.area.name if obj.area else "",
                event_datetime=obj.event_datetime,
            )
        except EventAreaModel.DoesNotExist as exc:
            raise ValidationError({"area": ["Event area does not exist."]}) from exc
        except ValidationError:
            raise

    def get_queryset(self, name_filter: str | None = None, order_by: str | None = None):
        queryset = self.model.objects.filter(status="open").select_related("area")

        if name_filter:
            queryset = queryset.filter(name__icontains=name_filter)

        if order_by:
            if order_by.lower() == "asc":
                queryset = queryset.order_by("event_datetime")
            elif order_by.lower() == "desc":
                queryset = queryset.order_by("-event_datetime")
        else:
            queryset = queryset.order_by("-event_datetime")

        return queryset

    def get_list(self, queryset=None) -> list[EventDTO]:
        if queryset is None:
            queryset = self.get_queryset()
        events = [
            EventDTO(
                id=obj.id,
                name=obj.name,
                status=obj.status,
                area_id=obj.area_id,
                area=obj.area.name if obj.area else "",
                event_datetime=obj.event_datetime,
            )
            for obj in queryset
        ]
        return events


class EventAreaRepository:
    model = EventAreaModel

    def create(self, dto: EventAreaDTO) -> EventAreaDTO:
        try:
            obj = self.model(name=dto.name)
            obj.full_clean()
            obj.save()
            return EventAreaDTO(id=obj.id, name=obj.name)
        except ValidationError:
            raise
