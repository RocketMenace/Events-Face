import json
import logging
import random
import time
from datetime import timedelta
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from celery import shared_task
from django.db import transaction
from django.utils import timezone

from ..core.settings import (
    NOTIFICATION_SERVICE_OWNER_ID,
    NOTIFICATION_SERVICE_URL,
    NOTIFICATION_TOKEN,
)
from ..events.models import EventModel
from ..notifications.models import NotificationModel

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

RETRYABLE_STATUSES = {429, 500, 502, 503, 504}
MAX_NOTIFICATION_ATTEMPTS = 5
BASE_BACKOFF_SECONDS = 1.0
MAX_BACKOFF_SECONDS = 30.0
REQUEST_TIMEOUT_SECONDS = 5.0


@shared_task(name="tasks.delete_old_events", queue="periodic")
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


def run_notifications_outbox_loop(sleep_interval: float = 1.0):
    notification_api_url = NOTIFICATION_SERVICE_URL
    notification_token = NOTIFICATION_TOKEN
    notifications_service_owner_id = NOTIFICATION_SERVICE_OWNER_ID

    while True:
        with transaction.atomic():
            notifications = (
                NotificationModel.objects.filter(sent=False)
                .select_for_update(skip_locked=True)
                .order_by("created_at")[:100]
            )

            if not notifications.exists():
                logger.info("No unsent notifications found. Sleeping...")
                time.sleep(1)
                continue

            logger.info(f"Processing {notifications.count()} notification(s)...")

            for notification in notifications:
                try:
                    request_data = {
                        "id": str(notification.id),
                        "email": notification.payload.get("email"),
                        "message": notification.payload.get("message"),
                        "owner_id": f"{notifications_service_owner_id}",
                    }
                    json_data = json.dumps(request_data).encode("utf-8")

                    status_code = _send_notification_with_retry(
                        url=notification_api_url,
                        payload=json_data,
                        token=notification_token,
                    )

                    if status_code == 200:
                        notification.sent = True
                        notification.sent_at = timezone.now()
                        notification.save()
                        logger.info(
                            "Successfully sent notification %s (topic: %s)",
                            notification.id,
                            notification.topic,
                        )
                    elif status_code == 401:
                        notification.sent = True
                        notification.sent_at = timezone.now()
                        notification.save()
                        logger.warning(
                            "Notification %s unauthorized (401). Marking as processed to avoid retries.",
                            notification.id,
                        )
                    else:
                        logger.error(
                            "Failed to send notification %s: API returned status code %s",
                            notification.id,
                            status_code,
                        )

                except HTTPError as e:
                    logger.error(
                        "HTTP error while processing notification %s: Status %s Reason %s",
                        notification.id,
                        e.code,
                        e.reason,
                    )
                except URLError as e:
                    logger.error(
                        "URL error while processing notification %s: %s",
                        notification.id,
                        e.reason,
                    )
                except Exception as e:
                    logger.error(
                        "Failed to process notification %s: %s",
                        notification.id,
                        e,
                        exc_info=True,
                    )

        time.sleep(sleep_interval)


def _send_notification_with_retry(url: str, payload: bytes, token: str) -> int:
    attempt = 1
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    while attempt <= MAX_NOTIFICATION_ATTEMPTS:
        req = Request(url, data=payload, headers=headers, method="POST")

        try:
            with urlopen(req, timeout=REQUEST_TIMEOUT_SECONDS) as response:
                return response.status
        except HTTPError as e:
            if e.code == 401:
                return e.code
            if e.code in RETRYABLE_STATUSES and attempt < MAX_NOTIFICATION_ATTEMPTS:
                delay = _calculate_backoff(attempt)
                logger.warning(
                    "Retryable HTTP error (%s). Attempt %s/%s. Retrying in %.2fs",
                    e.code,
                    attempt,
                    MAX_NOTIFICATION_ATTEMPTS,
                    delay,
                )
                time.sleep(delay)
                attempt += 1
                continue
            raise
        except URLError as e:
            if attempt < MAX_NOTIFICATION_ATTEMPTS:
                delay = _calculate_backoff(attempt)
                logger.warning(
                    "Network error (%s). Attempt %s/%s. Retrying in %.2fs",
                    e.reason,
                    attempt,
                    MAX_NOTIFICATION_ATTEMPTS,
                    delay,
                )
                time.sleep(delay)
                attempt += 1
                continue
            raise

    raise RuntimeError("Failed to send notification after maximum retries")


def _calculate_backoff(attempt: int) -> float:
    delay = min(BASE_BACKOFF_SECONDS * (2 ** (attempt - 1)), MAX_BACKOFF_SECONDS)
    jitter = random.uniform(0, 0.5)
    return delay + jitter
