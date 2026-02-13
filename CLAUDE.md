# Anny — Python FastAPI Application

## What This Project Does
Anny is a Python web application built with FastAPI. It provides a modern, high-performance API framework with automatic OpenAPI documentation, async support, and type-safe request/response handling.

## Architecture
```
Client → FastAPI → Route Handlers → Business Logic → Response
```

Architecture details will be filled in as the project develops.

## Project Structure
```
Anny/
├── CLAUDE.md                    # AI operating manual (this file — source of truth)
├── README.md                    # Comprehensive project docs
├── SECURITY.md                  # Security policy and controls
├── CHANGELOG.md                 # Version history
├── Makefile                     # Standard targets (test, lint, format, audit)
├── .pre-commit-config.yaml      # Format + lint + test on every commit
├── .gitignore                   # Python ignores
├── .env.example                 # Environment config template
├── pyproject.toml               # Python project config (pytest, black, pylint)
├── requirements.txt             # Production dependencies
├── requirements-dev.txt         # Dev/test dependencies
├── .github/
│   └── workflows/
│       └── ci.yml               # GitHub Actions CI pipeline
├── .vscode/
│   └── settings.json            # Editor config (format-on-save)
├── src/
│   └── anny/
│       ├── __init__.py
│       └── main.py              # FastAPI application entry point
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/
│   │   ├── __init__.py
│   │   └── test_main.py
│   ├── integration/
│   │   └── __init__.py
│   └── mocks/
├── scripts/
├── architecture/
└── docs/
    ├── manuals/
    ├── captains_log/
    ├── security/
    ├── reviews/
    ├── tickets/
    ├── budget/BUDGET.md
    └── pm/
        ├── FRAMEWORK.md
        ├── CURRENT-SPRINT.md
        ├── SPRINT-LOG.md
        └── BACKLOG.md
```

## Dev Environment
- Python 3.12+
- Package manager: pip with venv
- Install: `make install`
- Run tests: `make test`
- Run unit tests: `make unit`
- Run integration tests: `make integration`
- Format: `make format`
- Lint: `make lint`
- Start dev server: `make run`

## Key External APIs
- (none yet — add as project develops)

## Conventions
- Python: formatted with Black (line-length=100), linted with pylint
- Tests: pytest with pytest-cov
- Task runner: `make help` for all targets
- FastAPI app in `src/anny/main.py`
- Pre-commit hooks enforce format + lint + test on every commit

## Current Status (2026-02-13)
- **Code:** Initial scaffold. 1 placeholder test.
- **Pipeline:** GitHub Actions CI configured.
- **Deployment:** Not yet deployed.
- **Git:** GitHub repo, branch `main`
