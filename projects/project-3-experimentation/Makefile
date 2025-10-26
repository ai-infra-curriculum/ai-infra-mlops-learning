.PHONY: help install test lint format clean setup-infrastructure

help:
	@echo "Available commands:"
	@echo "  make install              - Install dependencies"
	@echo "  make test                 - Run tests"
	@echo "  make test-coverage        - Run tests with coverage"
	@echo "  make lint                 - Run linting"
	@echo "  make format               - Format code"
	@echo "  make type-check           - Run type checking"
	@echo "  make quality              - Run all quality checks"
	@echo "  make setup-infrastructure - Set up infrastructure services"
	@echo "  make clean                - Clean build artifacts"

install:
	pip install -e .
	pip install -e ".[dev]"

test:
	pytest tests/

test-coverage:
	pytest tests/ --cov=src --cov-report=html --cov-report=term

lint:
	flake8 src tests
	pylint src

format:
	black src tests
	isort src tests

type-check:
	mypy src

quality: format lint type-check test

setup-infrastructure:
	docker-compose up -d
	@echo "Waiting for services to start..."
	sleep 10
	alembic upgrade head

validate:
	python scripts/validate_config.py

clean:
	rm -rf build dist *.egg-info
	rm -rf .pytest_cache .coverage htmlcov
	find . -type d -name __pycache__ -exec rm -rf {} +
