import signal
import sys

from django.core.management.base import BaseCommand

from ....tasks.tasks import run_notifications_outbox_loop


class Command(BaseCommand):
    help = "Continuously processes unsent notifications from the outbox."

    def add_arguments(self, parser):
        parser.add_argument(
            "--sleep",
            type=float,
            default=1.0,
            help="Sleep interval (in seconds) between polling cycles.",
        )

    def handle(self, *args, **options):
        sleep_interval = options["sleep"]
        self.stdout.write(
            self.style.SUCCESS(
                f"Starting notifications outbox processor (sleep={sleep_interval}s)...",
            ),
        )

        signal.signal(signal.SIGINT, self._handle_exit)
        signal.signal(signal.SIGTERM, self._handle_exit)

        run_notifications_outbox_loop(sleep_interval=sleep_interval)

    def _handle_exit(self, signum, frame):
        self.stdout.write(self.style.WARNING("Received shutdown signal. Exiting..."))
        sys.exit(0)
