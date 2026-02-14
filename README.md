# Anny

**A modern Python web application built with FastAPI.**

Anny provides a high-performance, async-first API framework with automatic OpenAPI documentation, type-safe request/response handling, and production-ready conventions baked in from day one.

> **Status:** Initial scaffold. Not yet deployed.

---

## Table of Contents

- [How It Works](#how-it-works)
- [Features](#features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Installation and Setup](#installation-and-setup)
- [Configuration](#configuration)
- [Usage](#usage)
- [Testing](#testing)
- [Monitoring and Alerting](#monitoring-and-alerting)
- [Cost](#cost)
- [Security](#security)
- [Documentation](#documentation)
- [Contributing](#contributing)

---

## How It Works

Anny is a FastAPI application that serves as a web API. Requests flow through FastAPI's ASGI server, are routed to handler functions, processed through business logic, and return structured JSON responses.

## Features

- FastAPI with automatic OpenAPI/Swagger docs
- Async request handling
- Type-safe request/response models via Pydantic
- Health check endpoint
- Structured project layout
- Pre-commit hooks (Black + pylint + pytest)
- GitHub Actions CI pipeline
- Makefile with standard development targets

## Architecture

```
Client Request
    │
    ▼
FastAPI (ASGI)
    │
    ▼
Route Handlers (src/anny/main.py)
    │
    ▼
Business Logic
    │
    ▼
JSON Response
```

## Project Structure

```
Anny/
├── src/anny/          # Application source code
│   ├── __init__.py
│   └── main.py        # FastAPI app entry point
├── tests/             # Test suite
│   ├── unit/          # Unit tests
│   ├── integration/   # Integration tests
│   └── mocks/         # Test mocks and fixtures
├── docs/              # Documentation
│   ├── manuals/       # User and developer guides
│   ├── pm/            # Sprint management (Bolt framework)
│   ├── security/      # Security audit reports
│   ├── reviews/       # Code review logs
│   └── budget/        # Cost tracking
├── scripts/           # Utility scripts
└── architecture/      # Architecture diagrams
```

## Installation and Setup

### Prerequisites

- Python 3.12+
- pip

### Setup

```bash
# Clone the repository
git clone https://github.com/msichris/Anny.git
cd Anny

# Create virtual environment and install dependencies
make install

# Activate the virtual environment
source .venv/bin/activate
```

### Verify Installation

```bash
make test
```

## Configuration

Copy the example environment file and fill in your values:

```bash
cp .env.example .env
```

See `.env.example` for all available configuration options.

## Usage

### Start the Development Server

```bash
make run
```

The API will be available at `http://localhost:8000`.

### API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

### Health Check

```bash
curl http://localhost:8000/health
```

## Testing

```bash
# Run all tests
make test

# Run unit tests only
make unit

# Run integration tests only
make integration

# Run with coverage report
make test
```

## Monitoring and Alerting

(To be configured as the project develops.)

## Cost

See `docs/budget/BUDGET.md` for infrastructure cost tracking.

## Security

See `SECURITY.md` for the security policy, controls, and audit history.

## Documentation

| Document | Audience | Location |
|----------|----------|----------|
| README.md | Everyone | This file |
| CLAUDE.md | AI pair | Root |
| SECURITY.md | Security team | Root |
| Developer Guide | Engineers | `docs/manuals/` |
| Sprint Framework | PM/Dev | `docs/pm/FRAMEWORK.md` |

## Contributing

1. Create a feature branch from `main`
2. Make your changes
3. Ensure `make format-check && make lint && make test` passes
4. Submit a pull request

Pre-commit hooks will enforce formatting, linting, and tests automatically.

---

## License

MIT
