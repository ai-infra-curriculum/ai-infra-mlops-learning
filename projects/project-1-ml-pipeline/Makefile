.PHONY: help install install-dev setup clean test lint format type-check security-check

# Variables
PYTHON := python3
PIP := pip3
PYTEST := pytest
BLACK := black
FLAKE8 := flake8
MYPY := mypy
BANDIT := bandit

# Paths
SRC_DIR := src
TEST_DIR := tests
DOCS_DIR := docs

help:
	@echo "Available commands:"
	@echo "  make install          Install production dependencies"
	@echo "  make install-dev      Install development dependencies"
	@echo "  make setup            Complete setup (install + init)"
	@echo "  make clean            Remove generated files"
	@echo "  make test             Run all tests"
	@echo "  make test-unit        Run unit tests"
	@echo "  make test-integration Run integration tests"
	@echo "  make test-e2e         Run end-to-end tests"
	@echo "  make test-coverage    Run tests with coverage"
	@echo "  make lint             Run linting"
	@echo "  make format           Format code with black"
	@echo "  make type-check       Run type checking"
	@echo "  make security-check   Run security checks"
	@echo "  make check-all        Run all checks"
	@echo "  make train            Run training pipeline"
	@echo "  make serve            Start API server"
	@echo "  make docker-build     Build Docker images"
	@echo "  make docker-up        Start Docker services"
	@echo "  make docker-down      Stop Docker services"

# Installation
install:
	$(PIP) install -r requirements.txt

install-dev:
	$(PIP) install -r requirements-dev.txt

setup: install-dev
	@echo "Setting up project..."
	cp .env.example .env
	@echo "Please edit .env file with your configuration"
	@echo "Setup complete!"

# Cleaning
clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '*.egg-info' -exec rm -rf {} +
	find . -type d -name '.pytest_cache' -exec rm -rf {} +
	find . -type d -name '.mypy_cache' -exec rm -rf {} +
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf dist
	rm -rf build

clean-pyc:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

clean-test:
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage

# Testing
test:
	$(PYTEST) $(TEST_DIR) -v

test-unit:
	$(PYTEST) $(TEST_DIR)/unit -v -m unit

test-integration:
	$(PYTEST) $(TEST_DIR)/integration -v -m integration

test-e2e:
	$(PYTEST) $(TEST_DIR)/e2e -v -m e2e

test-coverage:
	$(PYTEST) $(TEST_DIR) --cov=$(SRC_DIR) --cov-report=html --cov-report=term-missing

# Code quality
lint:
	$(FLAKE8) $(SRC_DIR) $(TEST_DIR)

format:
	$(BLACK) $(SRC_DIR) $(TEST_DIR)

format-check:
	$(BLACK) $(SRC_DIR) $(TEST_DIR) --check

type-check:
	$(MYPY) $(SRC_DIR)

security-check:
	$(BANDIT) -r $(SRC_DIR)
	safety check

check-all: format-check lint type-check security-check test

# ML Pipeline operations
train:
	$(PYTHON) src/models/train.py

predict:
	$(PYTHON) src/models/predict.py

serve:
	uvicorn src.api.serve:app --host 0.0.0.0 --port 8000 --reload

# Data operations
ingest-data:
	$(PYTHON) src/data/ingestion.py

validate-data:
	$(PYTHON) src/data/validation.py

engineer-features:
	$(PYTHON) src/features/engineering.py

# Docker operations
docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

docker-ps:
	docker-compose ps

# Database operations
db-init:
	@echo "TODO: Initialize database schema"

db-migrate:
	@echo "TODO: Run database migrations"

db-reset:
	@echo "TODO: Reset database"

# Airflow operations
airflow-init:
	airflow db init
	airflow users create \
		--username admin \
		--firstname Admin \
		--lastname User \
		--role Admin \
		--email admin@example.com \
		--password admin

airflow-start:
	airflow webserver -p 8080 -D
	airflow scheduler -D

airflow-stop:
	pkill -f "airflow webserver"
	pkill -f "airflow scheduler"

# Health checks
health-check:
	@echo "Running health checks..."
	curl -f http://localhost:8000/health || echo "API not running"
	curl -f http://localhost:5000/health || echo "MLflow not running"
	curl -f http://localhost:8080/health || echo "Airflow not running"

# Documentation
docs-build:
	cd $(DOCS_DIR) && make html

docs-serve:
	cd $(DOCS_DIR)/_build/html && $(PYTHON) -m http.server

# Pipeline runs
pipeline-train:
	@echo "Running complete training pipeline..."
	$(MAKE) ingest-data
	$(MAKE) validate-data
	$(MAKE) engineer-features
	$(MAKE) train

pipeline-predict:
	@echo "Running batch prediction pipeline..."
	$(MAKE) predict

pipeline-monitor:
	@echo "Running monitoring pipeline..."
	$(PYTHON) src/monitoring/drift_detector.py
