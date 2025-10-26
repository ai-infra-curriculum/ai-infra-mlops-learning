.PHONY: help install install-dev test lint format clean validate check pre-commit

# Variables
PYTHON := python3
PIP := $(PYTHON) -m pip
VENV := venv
ACTIVATE := source $(VENV)/bin/activate

# Default target
help:
	@echo "AI Infrastructure MLOps Learning - Makefile Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install        Install production dependencies"
	@echo "  make install-dev    Install development dependencies"
	@echo "  make venv          Create virtual environment"
	@echo ""
	@echo "Development:"
	@echo "  make format        Format code with black and isort"
	@echo "  make lint          Run linters (flake8, pylint)"
	@echo "  make type-check    Run mypy type checking"
	@echo "  make test          Run pytest tests"
	@echo "  make coverage      Run tests with coverage report"
	@echo "  make security      Run security checks (bandit, safety)"
	@echo ""
	@echo "Quality:"
	@echo "  make check         Run all checks (format, lint, type, test)"
	@echo "  make validate      Validate all code and configuration"
	@echo "  make pre-commit    Run pre-commit hooks"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean         Remove generated files and caches"
	@echo "  make clean-all     Remove everything including venv"

# Setup
venv:
	$(PYTHON) -m venv $(VENV)
	@echo "Virtual environment created. Activate with: source $(VENV)/bin/activate"

install: venv
	$(ACTIVATE) && $(PIP) install --upgrade pip
	$(ACTIVATE) && $(PIP) install -r requirements.txt

install-dev: install
	$(ACTIVATE) && $(PIP) install -r requirements-dev.txt
	$(ACTIVATE) && $(PIP) install -e .
	$(ACTIVATE) && pre-commit install

# Code formatting
format:
	@echo "Running black..."
	black lessons/ --line-length 88
	@echo "Running isort..."
	isort lessons/ --profile black
	@echo "Formatting complete!"

format-check:
	@echo "Checking black formatting..."
	black --check lessons/ --line-length 88
	@echo "Checking isort..."
	isort --check-only lessons/ --profile black

# Linting
lint:
	@echo "Running flake8..."
	flake8 lessons/ --max-line-length=88 --extend-ignore=E203,W503
	@echo "Running pylint..."
	pylint lessons/ --max-line-length=88 --disable=C0114,C0115,C0116

# Type checking
type-check:
	@echo "Running mypy..."
	mypy lessons/ --ignore-missing-imports

# Testing
test:
	@echo "Running pytest..."
	pytest lessons/ -v

test-fast:
	@echo "Running fast tests only..."
	pytest lessons/ -v -m "not slow"

coverage:
	@echo "Running tests with coverage..."
	pytest lessons/ -v --cov=lessons --cov-report=term-missing --cov-report=html
	@echo "Coverage report generated in htmlcov/"

# Security
security:
	@echo "Running bandit security scan..."
	bandit -r lessons/ -f json -o bandit-report.json || true
	@echo "Running safety check..."
	safety check || true

# Combined checks
check: format-check lint type-check test
	@echo "All checks passed!"

validate: check security
	@echo "Validation complete!"

# Pre-commit
pre-commit:
	@echo "Running pre-commit hooks..."
	pre-commit run --all-files

pre-commit-install:
	pre-commit install

# Cleaning
clean:
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build dist htmlcov .coverage* bandit-report.json
	@echo "Cleanup complete!"

clean-all: clean
	rm -rf $(VENV)
	@echo "Full cleanup complete!"

# Documentation
docs:
	@echo "Building documentation..."
	mkdocs build
	@echo "Documentation built in site/"

docs-serve:
	@echo "Starting documentation server..."
	mkdocs serve

# Module-specific testing
test-module:
	@echo "Testing specific module..."
	@read -p "Enter module number (e.g., 01): " MODULE; \
	pytest lessons/$$MODULE*/ -v

# Quick development workflow
dev: format lint test
	@echo "Development checks complete!"
