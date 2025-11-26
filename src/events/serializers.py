from datetime import datetime

from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .dto import EventAreaDTO, EventDTO
from .models import EventAreaModel, EventModel


class EventAreaBaseSerializer(serializers.Serializer):
    name = serializers.CharField(
        max_length=255,
        required=True,
        allow_blank=False,
        trim_whitespace=True,
        allow_null=False,
    )


class EventAreaRequestSerializer(EventAreaBaseSerializer):
    name = serializers.CharField(
        max_length=255,
        required=True,
        allow_blank=False,
        trim_whitespace=True,
        allow_null=False,
        validators=[
            UniqueValidator(
                queryset=EventAreaModel.objects.all(),
                message=_("This name already exists. Please try another."),
            ),
        ],
    )

    def to_dto(self) -> EventAreaDTO:
        return EventAreaDTO(**self.validated_data)


class EventAreaResponseSerializer(EventAreaBaseSerializer):
    id = serializers.UUIDField()

    @classmethod
    def from_dto(cls, dto: EventAreaDTO) -> "EventAreaResponseSerializer | None":
        serializer = cls(data={"id": dto.id, "name": dto.name})
        if serializer.is_valid(raise_exception=True):
            return serializer
        return None


class EventBaseSerializer(serializers.Serializer):
    name = serializers.CharField(
        max_length=255,
        required=True,
        allow_blank=False,
        trim_whitespace=True,
        allow_null=True,
    )
    area_id = serializers.UUIDField(required=False, allow_null=True)
    status = serializers.ChoiceField(
        choices=EventModel.EventStatus.choices,
        default=EventModel.EventStatus.OPEN,
        required=False,
    )
    event_datetime = serializers.DateTimeField(
        required=True,
        format="%m.%d.%Y",
        input_formats=["%m.%d.%Y"],
        default_timezone=timezone.get_current_timezone(),
    )
    registration_deadline = serializers.DateTimeField(
        required=True,
        format="%m.%d.%Y",
        input_formats=["%m.%d.%Y"],
        default_timezone=timezone.get_current_timezone(),
    )

    @staticmethod
    def validate_event_datetime(value: datetime) -> datetime:
        if value < timezone.now():
            raise serializers.ValidationError(
                "Event datetime cannot be in the past.",
            )
        return value


class EventRequestSerializer(EventBaseSerializer):
    def to_dto(self) -> EventDTO:
        return EventDTO(**self.validated_data)


class EventResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    area = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    status = serializers.CharField()
    event_datetime = serializers.DateTimeField(
        format="%m.%d.%Y",
    )
    registration_deadline = serializers.DateTimeField(
        required=True,
        format="%m.%d.%Y",
        input_formats=["%m.%d.%Y"],
        default_timezone=timezone.get_current_timezone(),
    )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if not representation.get("area"):
            representation.pop("area", None)
        return representation

    @staticmethod
    def _dto_to_payload(dto: EventDTO) -> dict:
        return {
            "id": dto.id,
            "name": dto.name,
            "area": dto.area or "",
            "status": dto.status,
            "event_datetime": dto.event_datetime,
            "registration_deadline": dto.registration_deadline,
        }

    @classmethod
    def from_dto(cls, dto: EventDTO) -> "EventResponseSerializer | None":
        serializer = cls(data=cls._dto_to_payload(dto))
        if serializer.is_valid(raise_exception=True):
            return serializer
        return None

    @classmethod
    def from_dtos(cls, dtos: list[EventDTO]) -> "EventResponseSerializer | None":
        serializer = cls(
            data=[cls._dto_to_payload(dto=dto) for dto in dtos],
            many=True,
        )
        if serializer.is_valid(raise_exception=True):
            return serializer
        return None
