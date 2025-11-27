# Events-Face

Events-Face is a comprehensive event management system built with Django REST Framework. It provides APIs for managing events, event areas, visitor registrations, and notifications. The system includes background task processing, event synchronization, and integration with external notification services.

## Table of Contents

- [Project Description](#project-description)
- [Technical Stack](#technical-stack)
- [Technical Requirements](#technical-requirements)
- [Project Functionalities](#project-functionalities)
- [Installation and Setup](#installation-and-setup)
- [Deployment](#deployment)
- [API Documentation](#api-documentation)
- [Development](#development)

## Project Description

Events-Face is a RESTful API service for managing events and visitor registrations. The system allows:

- Creating and managing event areas (venues)
- Creating and listing events with filtering and pagination
- Visitor registration for events with validation
- Automatic notification processing via outbox pattern
- Event synchronization from external providers
- Scheduled cleanup of old events
- JWT-based authentication

The architecture follows clean architecture principles with separation of concerns using DTOs, repositories, services, and use cases. The system uses an outbox pattern for reliable notification delivery.

## Technical Stack

### Backend Framework
- **Django 5.2.8** - High-level Python web framework
- **Django REST Framework 3.16.1** - Toolkit for building Web APIs
- **Python 3.13+** - Programming language

### Database
- **PostgreSQL 15** - Primary relational database
- **Redis 7** - Message broker and cache for Celery

### Task Queue
- **Celery 5.5.3** - Distributed task queue
- **django-celery-beat 2.8.1** - Database-backed periodic task scheduler

### Authentication
- **djangorestframework-simplejwt 5.5.1** - JWT authentication for Django REST Framework

### API Documentation
- **drf-spectacular 0.29.0** - OpenAPI 3.0 schema generation for Django REST Framework

### Additional Libraries
- **django-environ 0.12.0** - Environment variable management
- **punq 0.7.0** - Dependency injection container
- **psycopg2-binary 2.9.11** - PostgreSQL adapter for Python


### Development Tools
- **ruff 0.14.6** - Fast Python linter and formatter
- **pre-commit 4.5.0** - Git hooks framework

### Infrastructure
- **Docker & Docker Compose** - Containerization and orchestration

## Technical Requirements

### System Requirements
- **Python**: 3.13 or higher
- **PostgreSQL**: 15 or higher
- **Redis**: 7 or higher
- **Docker**: 20.10 or higher (for containerized deployment)
- **Docker Compose**: 2.0 or higher

### Environment Variables

Copy variables from `.env.example` to `.env` file and setup your variables:

```bash
cp .env.example .env
```

Then edit the `.env` file with your configuration. The following variables need to be set:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
POSTGRES_DB=events_face
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-password
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# Redis & Celery Configuration
REDIS_PORT=6379
CELERY_BROKER_URL=redis://redis:6379/0

# External notification service
NOTIFICATION_SERVICE_URL=https://notifications.example.com/api/notifications
NOTIFICATION_TOKEN=changeme

# Application Port
APP_PORT=8000
```

## Project Functionalities

### 1. Event Management

#### Event Areas
- **Create Event Area**: Create a new event area (venue) with a unique name
- **List Event Areas**: View all event areas in the admin panel
- **Admin Panel**: Full CRUD operations for event areas

#### Events
- **Create Event**: Create a new event with:
  - Name, status (open/closed), event datetime
  - Registration deadline
  - Optional event area association
- **List Events**:
  - Paginated list of open events
  - Filter by name (case-insensitive partial match)
  - Sort by event datetime (ascending/descending)
  - Default ordering by event datetime (descending)

### 2. Visitor Registration

- **Sign Up for Event**: Register a visitor for a specific event
  - Validates event exists and is open
  - Prevents duplicate registrations (unique constraint on event + email)
  - Creates notification for successful registration
  - Returns confirmation message

**Validation Rules:**
- Event must exist
- Event must be open (status = "open")
- Email must be unique per event
- Full name and email are required

### 3. Authentication

- **User Registration**: Create new user accounts
- **User Login**: Authenticate and receive JWT tokens
- **Token Refresh**: Refresh access tokens
- **User Logout**: Invalidate tokens

### 4. Notifications

- **Outbox Pattern**: Notifications are stored in the database before sending
- **Dedicated Processing Loop**: `python manage.py process_notifications_outbox` continuously pushes unsent notifications to the external API (can run locally or in its own container)
- **Celery Integration**: The same logic is exposed as a Celery task (`tasks.process_notifications_outbox`) routed to the `notifications` queue and can be scheduled via Celery Beat
- **External API Integration**: Sends notifications to the configured notification service using bearer token authentication
- **Reliable Delivery**: Notifications are marked as sent only after the API confirms processing; failures are logged and retried on the next loop

### 5. Event Synchronization

- **Sync Command**: Management command to synchronize events from external provider
- **Incremental Sync**: Syncs only events changed since last sync
- **Full Sync**: Option to perform full synchronization of all events
- **Sync Results Tracking**: Records sync statistics (new events, updated events, last synced timestamp)

### 6. Scheduled Tasks

- **Delete Old Events**: Celery Beat enqueues the cleanup task every day (configurable schedule)
- **Process Notifications**: Celery Beat can trigger the outbox task periodically, while a dedicated management command/process can keep it running continuously

### 7. Admin Panel

- **Django Admin**: Full admin interface for:
  - Event Areas (with event count)
  - Events (with filtering, search, date hierarchy)
  - Visitors (with event association)
  - Notifications (with sent status)
  - Sync Results (with statistics)

## Installation and Setup

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Events-Face
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install uv
   uv pip install -e .
   ```

4. **Create `.env` file**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Set up database**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser** (optional, for admin access)
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

8. **Run Celery worker** (in separate terminal)
   ```bash
   celery -A src worker --loglevel=info
   ```

9. **Run Celery beat** (in separate terminal, for scheduled tasks)
   ```bash
   celery -A src beat --loglevel=info
   ```

### Using Makefile Commands

The project includes a Makefile with convenient commands:

```bash
# Run Django application
make run

# Run migrations
make migrate

# Create migrations
make makemigrations

# Create superuser
make csu

# Format code
make format

# Check code
make check

# Run tests
make test
```

## Deployment

### Docker Deployment

The project is configured for Docker deployment using Docker Compose.

#### Prerequisites
- Docker 20.10+
- Docker Compose 2.0+

#### Steps

1. **Create `.env` file**
   ```bash
   # Copy variables from .env.example to .env file
   cp .env.example .env
   # Edit .env with your production values
   ```

2. **Build Docker images**
   ```bash
   docker-compose build
   # Or using Makefile:
   make build
   ```

3. **Start all services**
   ```bash
   docker-compose up -d
   # Or using Makefile:
   make run_all
   ```

4. **Run migrations**
   ```bash
   docker-compose exec events_face python manage.py migrate
   ```

5. **Create superuser** (optional)
   ```bash
   docker-compose exec events_face python manage.py createsuperuser
   ```

6. **Collect static files** (if needed)
   ```bash
   docker-compose exec events_face python manage.py collectstatic --noinput
   ```

#### Docker Services

The `docker-compose.yaml` includes the following services:

- **events_face**: Django application server (runs migrations & collectstatic once)
- **postgres**: PostgreSQL database
- **redis**: Redis cache and message broker
- **celery_beat**: Celery Beat scheduler (does not run migrations)
- **celery_worker_periodic**: Worker bound to the `periodic` queue (e.g., cleanup tasks)
- **celery_worker_notifications**: Worker bound to the `notifications` queue (outbox processing)
- *(optional custom service)* `notifications_outbox`: you can add a container that runs `python manage.py process_notifications_outbox --sleep 1` for a dedicated long-running outbox processor

#### Useful Docker Commands

```bash
# View running containers
docker-compose ps

# View logs
docker-compose logs -f events_face
docker-compose logs -f celery_worker_1

# Stop services
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop and remove containers, volumes, and networks
docker-compose down -v

# Restart services
docker-compose restart
```

### Production Considerations

1. **Environment Variables**: Ensure all sensitive data is in environment variables
2. **SECRET_KEY**: Use a strong, randomly generated secret key
3. **DEBUG**: Set to `False` in production
4. **ALLOWED_HOSTS**: Configure with your domain(s)
5. **Database**: Use managed database service or ensure proper backups
6. **Static Files**: Configure static file serving (e.g., via Nginx or CDN)
7. **SSL/TLS**: Use HTTPS in production
8. **Monitoring**: Set up logging and monitoring for Celery workers
9. **Scaling**: Adjust Celery worker concurrency based on load

## API Documentation

### Interactive API Documentation

Once the server is running, access the API documentation at:

- **Swagger UI**: `http://localhost:8000/api/swagger/`
- **ReDoc**: `http://localhost:8000/api/redoc/`
- **OpenAPI Schema**: `http://localhost:8000/api/schema/`

### API Endpoints

#### Events

- `GET /api/events/list` - List events (with pagination, filtering, sorting)
- `POST /api/events/` - Create a new event
- `POST /api/events/areas/` - Create a new event area
- `POST /api/events/<event_id>/register` - Register a visitor for an event

#### Authentication

- `POST /api/auth/register/` - Register a new user
- `POST /api/auth/login/` - Login and get JWT tokens
- `POST /api/auth/logout/` - Logout and invalidate tokens
- `POST /api/auth/refresh/` - Refresh access token

### Example API Requests

#### Create Event Area
```bash
curl -X POST http://localhost:8000/api/events/areas/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Main Hall"}'
```

#### Create Event
```bash
curl -X POST http://localhost:8000/api/events/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tech Conference 2025",
    "area_id": "1c74b3ec-b651-4775-88b6-8b21f37fc3f4",
    "status": "open",
    "event_datetime": "01.13.2026",
    "registration_deadline": "01.13.2026"
  }'
```

#### List Events
```bash
curl -X GET "http://localhost:8000/api/events/list?name=Tech&order_by=desc&limit=10&offset=0"
```

#### Register for Event
```bash
curl -X POST http://localhost:8000/api/events/<event_id>/register \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Doe",
    "email": "john.doe@example.com"
  }'
```

## Development

### Code Style

The project uses `ruff` for linting and formatting:

```bash
# Format code
ruff format .

# Check and fix code
ruff check --fix .
```

### Running Tests

```bash
# Run all tests
pytest

# Or using Makefile
make test
```

### Project Structure

```
Events-Face/
├── src/
│   ├── authentication/    # User authentication app
│   ├── common/            # Shared utilities and base classes
│   ├── core/              # Django project settings
│   ├── events/            # Events management app
│   ├── notifications/     # Notifications app
│   ├── sync/              # Event synchronization app
│   ├── tasks/             # Celery tasks
│   └── urls.py            # Main URL configuration
├── docker-compose.yaml    # Docker Compose configuration
├── Dockerfile             # Docker image definition
├── Makefile              # Make commands
├── manage.py             # Django management script
├── pyproject.toml        # Project dependencies
└── README.md             # This file
```

### Architecture

The project follows clean architecture principles:

- **DTOs**: Data Transfer Objects for data validation and transfer
- **Repositories**: Data access layer abstraction
- **Services**: Business logic layer
- **Use Cases**: Application-specific business rules
- **Views**: API endpoint handlers
- **Serializers**: Request/response validation and serialization

### Database Migrations

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### Management Commands

```bash
# Sync events from external provider
python manage.py run_sync_events

# Sync all events (full sync)
python manage.py run_sync_events --all

# Continuously process notification outbox (optional sleep interval)
python manage.py process_notifications_outbox --sleep 1
```

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]

## Support

[Add support information here]
