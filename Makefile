

.PHONY: help build run down destroy stop restart ps test migrate makemigrations csu run_all load_tariffs create_tasks create_bucket

help:
	@echo "Available commands:"
	@echo "  build             - Build the Docker images"
	@echo "  up                - Start all containers in detached mode"
	@echo "  down              - Stop and remove containers"
	@echo "  destroy           - Stop and remove containers, networks, volumes"
	@echo "  stop              - Stop running containers"
	@echo "  restart           - Restart containers"
	@echo "  ps                - List containers"
	@echo "  test              - Run Django tests"
	@echo "  migrate           - Run Django migrations"
	@echo "  makemigrations    - Create new Django migrations"
	@echo "  collectstatic     - Collect static files"
	@echo "  createsuperuser   - Create Django superuser"
	@echo "  run               - Run Django application locally"
	@echo "  format            - Run ruff format command"
	@echo "  check             - Run ruff check command"

run_all:
	docker-compose up -d

build:
	docker-compose build

run:
	python3 manage.py runserver

down:
	docker-compose down

destroy:
	docker-compose down -v

stop:
	docker-compose stop

restart:
	docker-compose restart

ps:
	docker-compose ps

test:
	pytest

migrate:
	python3 manage.py migrate

makemigrations:
	python3 manage.py makemigrations

csu:
	python3 manage.py csu

format:
	ruff format .

check:
	ruff check --fix .