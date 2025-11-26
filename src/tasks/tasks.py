import logging
from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from ..events.models import EventModel

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


@shared_task(name="tasks.delete_old_events")
def delete_old_events(days: int = 7) -> int:
    cutoff_date = timezone.now() - timedelta(days=days)
    logger.info(
        f"Starting deletion of events older than {cutoff_date} (>{days} days ago)",
    )

    deleted_count, deleted_objects = EventModel.objects.filter(
        event_datetime__lt=cutoff_date,
    ).delete()

    logger.info(
        f"Deleted {deleted_count} event(s). "
        f"Deleted objects breakdown: {deleted_objects}",
    )

    return deleted_count
