.PHONY: help install test unit integration e2e smoke lint format format-check audit clean run mcp docker-build docker-run provision setup deploy ssl-setup

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

e2e: ## Run e2e tests (requires ANNY_E2E=1 and real credentials)
	ANNY_E2E=1 .venv/bin/pytest tests/e2e/ -v --tb=short

smoke: ## Run smoke test against live server
	./scripts/smoke_test.sh

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

mcp: ## Start the MCP server in stdio mode
	.venv/bin/python -m anny.cli.mcp_stdio

docker-build: ## Build Docker image
	docker build -t anny .

docker-run: ## Run with Docker Compose
	docker compose up -d

provision: ## Provision Vultr VPS and DNS (requires VULTR_API_KEY)
	./scripts/server-provision.sh

setup: ## Bootstrap VPS with Docker, nginx, UFW, fail2ban
	./scripts/server-setup.sh

deploy: ## Deploy/update app on VPS
	./scripts/deploy.sh

ssl-setup: ## Obtain SSL cert and enable HTTPS (requires CERTBOT_EMAIL)
	./scripts/ssl-setup.sh
