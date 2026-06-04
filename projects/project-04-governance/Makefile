.PHONY: install test lint type up down logs reset

install:
	pip install -r requirements-dev.txt

test:
	pytest tests/ -v --cov=src --cov-report=term-missing

lint:
	ruff check src/ tests/

type:
	mypy src/

up:
	docker compose up -d --build

down:
	docker compose down -v

logs:
	docker compose logs -f api

reset:
	docker compose down -v && docker compose up -d --build
