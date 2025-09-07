# Makefile for Kepler-Downloader-DR25
# Run 'make help' for a list of commands

.PHONY: help clean install dev-install test lint format check-quality build upload-pypi

# Variables
PYTHON := python3
PIP := $(PYTHON) -m pip
PROJECT := kepler_downloader_dr25

# Default target
help:
	@echo "Kepler-Downloader-DR25 Development Commands"
	@echo "==========================================="
	@echo ""
	@echo "Setup:"
	@echo "  make install        Install package in production mode"
	@echo "  make dev-install    Install package in development mode with dev dependencies"
	@echo ""
	@echo "Testing:"
	@echo "  make test          Run all tests"
	@echo "  make test-cov      Run tests with coverage report"
	@echo "  make test-fast     Run tests without coverage"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint          Run flake8 linter"
	@echo "  make format        Format code with black and isort"
	@echo "  make check-quality Run all quality checks (lint + format check)"
	@echo "  make pre-commit    Install and run pre-commit hooks"
	@echo ""
	@echo "Build & Release:"
	@echo "  make build         Build distribution packages"
	@echo "  make clean         Clean build artifacts and cache files"
	@echo "  make upload-test   Upload to TestPyPI"
	@echo "  make upload-pypi   Upload to PyPI (use with caution)"
	@echo ""
	@echo "Development:"
	@echo "  make redis-start   Start Redis server (macOS)"
	@echo "  make redis-check   Check Redis connection"

# Installation targets
install:
	$(PIP) install -r requirements.txt
	$(PIP) install -e .

dev-install:
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements-dev.txt
	$(PIP) install -e .
	pre-commit install

# Testing targets
test:
	pytest tests/ -v --cov=$(PROJECT) --cov-report=term-missing

test-cov:
	pytest tests/ -v --cov=$(PROJECT) --cov-report=html --cov-report=term
	@echo "Coverage report generated in htmlcov/index.html"

test-fast:
	pytest tests/ -v

# Code quality targets
lint:
	flake8 $(PROJECT) tests

format:
	black $(PROJECT) tests --line-length 120
	isort $(PROJECT) tests --profile black --line-length 120

check-quality:
	black $(PROJECT) tests --check --line-length 120
	isort $(PROJECT) tests --check --profile black --line-length 120
	flake8 $(PROJECT) tests

pre-commit:
	pre-commit install
	pre-commit run --all-files

# Build targets
build: clean
	$(PYTHON) -m build

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

# Upload targets
upload-test: build
	$(PYTHON) -m twine upload --repository testpypi dist/*

upload-pypi: build
	@echo "WARNING: This will upload to PyPI. Are you sure? [y/N]"
	@read ans && [ $${ans:-N} = y ]
	$(PYTHON) -m twine upload dist/*

# Redis helpers
redis-start:
	@echo "Starting Redis server..."
	@if command -v brew >/dev/null 2>&1; then \
		brew services start redis; \
	else \
		echo "Please start Redis manually or use: sudo systemctl start redis"; \
	fi

redis-check:
	@echo "Checking Redis connection..."
	@redis-cli ping || echo "Redis is not running. Run 'make redis-start'"

# Development shortcuts
.PHONY: t l f c
t: test-fast
l: lint
f: format
c: check-quality