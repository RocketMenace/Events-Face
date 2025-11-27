#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

prepare_celery_beat_schedule() {
    local schedule_path="${CELERY_BEAT_SCHEDULE_PATH:-}"
    if [ -z "$schedule_path" ]; then
        return
    fi

    print_info "Preparing Celery beat schedule at ${schedule_path}"
    local schedule_dir
    schedule_dir=$(dirname "$schedule_path")

    mkdir -p "$schedule_dir" || {
        print_warn "Unable to create directory ${schedule_dir}"
        return
    }

    if [ -d "$schedule_path" ]; then
        print_warn "Existing schedule path ${schedule_path} is a directory. Removing..."
        rm -rf "$schedule_path" || print_warn "Failed to remove directory ${schedule_path}"
    fi

    if [ ! -f "$schedule_path" ]; then
        touch "$schedule_path" || print_warn "Failed to create schedule file ${schedule_path}"
    fi

    chown appuser:appuser "$schedule_path" 2>/dev/null || true
    chmod 664 "$schedule_path" 2>/dev/null || true
}

# Function to wait for PostgreSQL to be ready
wait_for_postgres() {
    print_info "Waiting for PostgreSQL to be ready..."

    until python -c "
import sys
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.core.settings')
import django
django.setup()
from django.db import connection
try:
    connection.ensure_connection()
    sys.exit(0)
except Exception:
    sys.exit(1)
" 2>/dev/null; do
        print_warn "PostgreSQL is unavailable - sleeping"
        sleep 1
    done

    print_info "PostgreSQL is up and running!"
}

# Function to wait for Redis to be ready
wait_for_redis() {
    print_info "Waiting for Redis to be ready..."

    until python -c "
import redis
import os
try:
    r = redis.Redis.from_url(os.environ.get('CELERY_BROKER_URL', 'redis://redis:6379/0'))
    r.ping()
    exit(0)
except Exception:
    exit(1)
" 2>/dev/null; do
        print_warn "Redis is unavailable - sleeping"
        sleep 1
    done

    print_info "Redis is up and running!"
}

# Function to run migrations
run_migrations() {
    print_info "Running database migrations..."
    python manage.py migrate --noinput
    print_info "Migrations completed successfully!"
}

# Function to collect static files
collect_static() {
    print_info "Collecting static files..."
    python manage.py collectstatic --noinput --clear || print_warn "Static files collection failed or not needed"
    print_info "Static files collected!"
}

# Main execution
main() {
    print_info "Starting Events-Face application..."

    local startup_delay="${STARTUP_DELAY:-0}"
    local wait_postgres="${WAIT_FOR_POSTGRES:-true}"
    local wait_redis="${WAIT_FOR_REDIS:-true}"
    local run_migrations_flag="${RUN_MIGRATIONS:-true}"
    local collect_static_flag="${COLLECT_STATIC:-false}"

    if [ "$startup_delay" != "0" ]; then
        print_info "Startup delay enabled. Sleeping for ${startup_delay}s..."
        sleep "$startup_delay"
    fi

    prepare_celery_beat_schedule

    if [ "$wait_postgres" = "true" ]; then
        wait_for_postgres
    else
        print_info "Skipping PostgreSQL wait (WAIT_FOR_POSTGRES=false)"
    fi

    if [ "$wait_redis" = "true" ]; then
        wait_for_redis
    else
        print_info "Skipping Redis wait (WAIT_FOR_REDIS=false)"
    fi

    if [ "$run_migrations_flag" = "true" ]; then
        run_migrations
    else
        print_info "Skipping migrations (RUN_MIGRATIONS=false)"
    fi

    if [ "$collect_static_flag" = "true" ]; then
        collect_static
    else
        print_info "Skipping static files collection (COLLECT_STATIC=false)"
    fi

    if [ "$#" -eq 0 ]; then
        set -- python manage.py runserver 0.0.0.0:8000
    fi

    print_info "Starting command: $*"
    exec "$@"
}

# Handle signals for graceful shutdown
trap 'print_warn "Received shutdown signal, shutting down gracefully..."; exit 0' SIGTERM SIGINT

# Run main function
main "$@"

