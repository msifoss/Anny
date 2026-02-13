.PHONY: help install test unit integration lint format format-check audit clean run

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install all dependencies
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt
	.venv/bin/pip install -r requirements-dev.txt
	.venv/bin/pip install -e .
	.venv/bin/pre-commit install

test: ## Run all tests
	.venv/bin/pytest tests/ -v --tb=short --cov=src/anny --cov-report=term-missing

unit: ## Run unit tests only
	.venv/bin/pytest tests/unit/ -v --tb=short

integration: ## Run integration tests only
	.venv/bin/pytest tests/integration/ -v --tb=short

lint: ## Run linter
	.venv/bin/pylint src/anny/ tests/

format: ## Format code
	.venv/bin/black src/ tests/

format-check: ## Check formatting (CI-friendly)
	.venv/bin/black --check src/ tests/

audit: ## Run dependency vulnerability scan
	.venv/bin/pip-audit

clean: ## Remove build artifacts
	rm -rf build/ dist/ *.egg-info .pytest_cache htmlcov .coverage .mypy_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

run: ## Start the development server
	.venv/bin/uvicorn src.anny.main:app --reload --host 0.0.0.0 --port 8000
