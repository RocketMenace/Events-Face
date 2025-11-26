import json
from datetime import datetime
from urllib.parse import urlencode
from urllib.request import urlopen
from uuid import UUID

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from src.events.models import EventAreaModel, EventModel
from src.sync.models import SyncResults


class Command(BaseCommand):
    help = "Synchronize events from events-provider service"

    def add_arguments(self, parser):
        parser.add_argument(
            "--all",
            action="store_true",
            help="Perform full synchronization of all events",
        )

    def handle(self, *args, **options):
        self.stdout.write("Starting events synchronization...")

        sync_all = options["all"]
        last_sync_result = SyncResults.objects.order_by("-created_at").first()

        if sync_all:
            self.stdout.write("Performing full synchronization...")
            url = "https://events.k3scluster.tech/api/events/"
        else:
            if last_sync_result and last_sync_result.last_synced_changed_at:
                changed_at_date = last_sync_result.last_synced_changed_at.date()
                self.stdout.write(
                    f"Performing incremental sync from {changed_at_date}...",
                )
                params = urlencode({"changed_at": changed_at_date.isoformat()})
                url = f"https://events.k3scluster.tech/api/events/?{params}"
            else:
                self.stdout.write(
                    "No previous sync found. Performing full synchronization...",
                )
                url = "https://events.k3scluster.tech/api/events/"

        try:
            events_data = self._fetch_events(url)
            self.stdout.write(f"Fetched {len(events_data)} events from API")

            new_count = 0
            updated_count = 0
            max_changed_at = None

            for event_data in events_data:
                result = self._sync_event(event_data)
                if result is None:
                    continue

                is_new, event_changed_at = result
                if is_new:
                    new_count += 1
                else:
                    updated_count += 1

                if event_changed_at:
                    if max_changed_at is None or event_changed_at > max_changed_at:
                        max_changed_at = event_changed_at

            if max_changed_at is None and last_sync_result:
                max_changed_at = last_sync_result.last_synced_changed_at

            sync_result = SyncResults.objects.create(
                new_events_count=new_count,
                updated_events_count=updated_count,
                last_synced_changed_at=max_changed_at,
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Sync completed successfully!\n"
                    f"  New events: {new_count}\n"
                    f"  Updated events: {updated_count}\n"
                    f"  Sync ID: {sync_result.id}",
                ),
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Sync failed: {str(e)}"),
            )
            raise CommandError(f"Synchronization failed: {str(e)}")

    def _fetch_events(self, url: str) -> list[dict]:
        try:
            with urlopen(url) as response:
                if response.status != 200:
                    raise CommandError(
                        f"API returned status code {response.status}",
                    )
                data = json.loads(response.read().decode("utf-8"))
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict) and "results" in data:
                    return data["results"]
                else:
                    raise CommandError(f"Unexpected API response format: {data}")
        except Exception as e:
            raise CommandError(f"Failed to fetch events from API: {str(e)}")

    def _sync_event(self, event_data: dict) -> tuple[bool, datetime | None] | None:
        event_id_str = event_data.get("id")
        if not event_id_str:
            self.stdout.write(
                self.style.WARNING("Skipping event without ID"),
            )
            return None

        try:
            event_id = UUID(str(event_id_str))
        except (ValueError, TypeError):
            self.stdout.write(
                self.style.WARNING(f"Skipping event with invalid ID: {event_id_str}"),
            )
            return None

        changed_at_str = event_data.get("changed_at")
        changed_at = None
        if changed_at_str:
            changed_at = parse_datetime(changed_at_str)
            if changed_at and timezone.is_naive(changed_at):
                changed_at = timezone.make_aware(changed_at)

        event_datetime_str = event_data.get("event_datetime")
        if not event_datetime_str:
            self.stdout.write(
                self.style.WARNING(f"Skipping event {event_id} without event_datetime"),
            )
            return None

        event_datetime = parse_datetime(event_datetime_str)
        if event_datetime and timezone.is_naive(event_datetime):
            event_datetime = timezone.make_aware(event_datetime)

        area = None
        area_data = event_data.get("area")
        if area_data:
            if isinstance(area_data, str):
                area_name = area_data
            elif isinstance(area_data, dict):
                area_name = area_data.get("name") or area_data.get("area")
            else:
                area_name = None

            if area_name:
                area, _ = EventAreaModel.objects.get_or_create(name=area_name)

        try:
            event = EventModel.objects.get(id=event_id)
            is_new = False

            event.name = event_data.get("name", event.name)
            event.status = event_data.get("status", event.status)
            event.event_datetime = event_datetime
            event.area = area
            event.save()

        except EventModel.DoesNotExist:
            is_new = True

            event = EventModel.objects.create(
                id=event_id,
                name=event_data.get("name", ""),
                status=event_data.get("status", EventModel.EventStatus.OPEN),
                event_datetime=event_datetime,
                area=area,
            )

        return is_new, changed_at
