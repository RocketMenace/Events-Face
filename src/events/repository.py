from uuid import UUID

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.core.exceptions import ValidationError

from .dto import EventAreaDTO, EventDTO, VisitorDTO
from .models import EventAreaModel, EventModel, VisitorModel


class EventRepository:
    model = EventModel

    def create(self, dto: EventDTO) -> EventDTO:
        try:
            obj = self.model(
                name=dto.name,
                status=dto.status,
                area_id=dto.area_id,
                event_datetime=dto.event_datetime,
                registration_deadline=dto.registration_deadline,
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
                registration_deadline=obj.registration_deadline,
            )
        except EventAreaModel.DoesNotExist as exc:
            raise ValidationError({"area": ["Event area does not exist."]}) from exc
        except ValidationError:
            raise

    def get_queryset(self, name_filter: str | None = None, order_by: str | None = None):
        queryset = self.model.objects.filter(status="open").select_related("area")

        if name_filter:
            search_vector = SearchVector("name")
            search_query = SearchQuery(name_filter)
            queryset = (
                queryset.annotate(
                    search=search_vector,
                    rank=SearchRank(search_vector, search_query),
                )
                .filter(search=search_query)
                .order_by("-rank", "-event_datetime")
            )

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
                registration_deadline=obj.registration_deadline,
            )
            for obj in queryset
        ]
        return events

    def get_open_events(self, event_id: UUID) -> bool:
        if not self.model.objects.filter(status="open", id=event_id):
            return False
        return True


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


class VisitorRepository:
    model = VisitorModel

    def create(self, dto: VisitorDTO) -> VisitorDTO:
        try:
            event = EventModel.objects.get(id=dto.event_id)
            obj = self.model(
                full_name=dto.full_name,
                email=dto.email,
                event_id=event,
            )
            obj.full_clean()
            obj.save()
            return VisitorDTO(
                id=obj.id,
                email=obj.email,
                full_name=obj.full_name,
                event_id=obj.event_id,
            )
        except EventModel.DoesNotExist as exc:
            raise ValidationError({"event_id": ["Event does not exist."]}) from exc
        except Exception:
            raise

    def is_visitor_registered(self, dto: VisitorDTO) -> bool:
        if self.model.objects.filter(email=dto.email, event_id=dto.event_id).first():
            return True
        return False
