from datetime import datetime
from uuid import UUID

from django.utils import timezone
from rest_framework import serializers

from .models import Event, EventArea


class EventAreaBaseSerializer(serializers.Serializer):
    name = serializers.CharField(
        max_length=255,
        required=True,
        allow_blank=False,
        trim_whitespace=True,
    )


class EventAreaRequestSerializer(EventAreaBaseSerializer):
    pass


class EventAreaResponseSerializer(EventAreaBaseSerializer):
    id = serializers.UUIDField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class EventBaseSerializer(serializers.Serializer):
    name = serializers.CharField(
        max_length=255,
        required=True,
        allow_blank=False,
        trim_whitespace=True,
    )
    area = serializers.UUIDField(required=True)
    status = serializers.ChoiceField(
        choices=Event.EventStatus.choices,
        default=Event.EventStatus.OPEN,
        required=False,
    )
    event_datetime = serializers.DateTimeField(required=True)

    @staticmethod
    def validate_area(value: UUID) -> UUID:
        try:
            EventArea.objects.get(id=value)
        except EventArea.DoesNotExist:
            raise serializers.ValidationError("Event area does not exist.")
        return value

    @staticmethod
    def validate_event_datetime(value: datetime) -> datetime:
        if value < timezone.now():
            raise serializers.ValidationError(
                "Event datetime cannot be in the past.",
            )
        return value


class EventRequestSerializer(EventBaseSerializer):
    pass


class EventResponseSerializer(EventBaseSerializer):
    id = serializers.UUIDField(read_only=True)
    area = serializers.UUIDField(read_only=True)
    area_name = serializers.CharField(source="area.name", read_only=True)
    status_display = serializers.CharField(
        read_only=True,
    )
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
