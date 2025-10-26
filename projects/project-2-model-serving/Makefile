.PHONY: help install test lint format clean docker-build docker-run k8s-deploy

help:
	@echo "Available commands:"
	@echo "  install        Install dependencies"
	@echo "  test          Run all tests"
	@echo "  test-unit     Run unit tests"
	@echo "  test-integration  Run integration tests"
	@echo "  lint          Run linters"
	@echo "  format        Format code"
	@echo "  clean         Clean up generated files"
	@echo "  docker-build  Build Docker image"
	@echo "  docker-run    Run with Docker Compose"
	@echo "  k8s-deploy    Deploy to Kubernetes"
	@echo "  run-local     Run locally"

install:
	pip install -r requirements-dev.txt

test:
	pytest tests/ -v

test-unit:
	pytest tests/unit/ -v

test-integration:
	pytest tests/integration/ -v

test-coverage:
	pytest tests/ --cov=src --cov-report=html --cov-report=term

lint:
	flake8 src/ tests/
	pylint src/
	mypy src/
	bandit -r src/

format:
	black src/ tests/
	isort src/ tests/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf .pytest_cache
	rm -rf .coverage htmlcov
	rm -rf dist build *.egg-info

docker-build:
	docker build -t model-server:latest .

docker-run:
	docker-compose up -d

docker-stop:
	docker-compose down

k8s-deploy:
	kubectl apply -f infrastructure/kubernetes/

k8s-delete:
	kubectl delete -f infrastructure/kubernetes/

run-local:
	bash scripts/run-local.sh

# Development helpers
dev-setup: install
	pre-commit install
	cp .env.example .env
	@echo "Development environment ready!"
	@echo "Edit .env with your configuration"

dev-services:
	docker-compose up -d postgres redis minio vault prometheus grafana

# Load testing
load-test:
	locust -f tests/load/locustfile.py --host=http://localhost:8000

# Database
db-init:
	python scripts/init-db.py

db-migrate:
	alembic upgrade head

db-rollback:
	alembic downgrade -1
