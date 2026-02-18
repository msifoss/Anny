# Anny — Conversational Analytics Tool

## What This Project Does
Anny is a conversational analytics tool that gives LLMs (via MCP) and programmatic clients (via REST API) access to Google Analytics 4, Google Search Console, and Google Tag Manager data using service account authentication.

## Architecture
```
┌─────────────────┐     ┌──────────────────┐
│  FastAPI REST    │     │  MCP Server      │
│  /api/ga4/...   │     │  (FastMCP)       │
│  /api/sc/...    │     │  HTTP at /mcp    │
│  /api/gtm/...   │     │  or stdio        │
└────────┬────────┘     └────────┬─────────┘
         │                       │
         └───────────┬───────────┘
                     ▼
         ┌───────────────────────┐
         │    Service Layer      │
         │  ga4_service          │
         │  search_console_svc   │
         │  tag_manager_svc      │
         │  memory_service       │
         └───────────┬───────────┘
                     ▼
         ┌───────────────────────┐
         │    Client Layer       │
         │  GA4Client            │
         │  SearchConsoleClient  │
         │  TagManagerClient     │
         │  MemoryStore (JSON)   │
         └───────────┬───────────┘
                     ▼
         ┌───────────────────────┐
         │  Auth (core/auth.py)  │
         │  Single service acct  │
         └───────────┬───────────┘
                     ▼
         ┌───────────────────────┐
         │  Config (pydantic-    │
         │  settings + .env)     │
         └───────────────────────┘
```

Both REST and MCP share the same service layer — zero duplication of Google API logic.

## Project Structure
```
Anny/
├── CLAUDE.md                    # AI operating manual (this file — source of truth)
├── README.md                    # Comprehensive project docs
├── SECURITY.md                  # Security policy and controls
├── CHANGELOG.md                 # Version history
├── Makefile                     # Standard targets (test, lint, format, audit, mcp)
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
│       ├── main.py              # FastAPI app, mounts routers + MCP
│       ├── mcp_server.py        # FastMCP instance + all MCP tools
│       ├── api/
│       │   ├── __init__.py
│       │   ├── models.py        # Pydantic request/response models
│       │   ├── error_handlers.py # AnnyError → HTTP status mapping
│       │   ├── ga4_routes.py    # GA4 REST endpoints
│       │   ├── search_console_routes.py
│       │   └── tag_manager_routes.py
│       ├── clients/
│       │   ├── __init__.py
│       │   ├── ga4.py           # GA4Client (Google Analytics Data API)
│       │   ├── memory.py        # MemoryStore (JSON file-backed memory)
│       │   ├── search_console.py # SearchConsoleClient
│       │   └── tag_manager.py   # TagManagerClient (GTM API v2)
│       ├── cli/
│       │   ├── __init__.py
│       │   └── mcp_stdio.py    # Standalone stdio entry point
│       └── core/
│           ├── __init__.py
│           ├── auth.py          # Service account credential loading
│           ├── config.py        # Settings(BaseSettings) from env
│           ├── date_utils.py    # Named date range parsing
│           ├── dependencies.py  # Lazy singleton client factories
│           ├── exceptions.py    # AnnyError, AuthError, APIError
│           ├── formatting.py    # Text table formatting for MCP
│           └── services/
│               ├── __init__.py
│               ├── ga4_service.py
│               ├── memory_service.py
│               ├── search_console_service.py
│               └── tag_manager_service.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/                    # 116 unit tests
│   ├── integration/             # 11 integration tests
│   └── mocks/
├── scripts/
├── architecture/
└── docs/
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
- Start MCP stdio server: `make mcp`

## Key External APIs
- Google Analytics Data API v1beta (GA4 reports)
- Google Search Console API v1 (search analytics)
- Google Tag Manager API v2 (accounts, containers, tags, triggers, variables)
- All via service account auth (readonly scopes)

## MCP Tools
| Tool | Purpose |
|------|---------|
| `ping` | Health check |
| `ga4_report` | Custom GA4 report (metrics, dimensions, date range) |
| `ga4_top_pages` | Top pages by page views |
| `ga4_traffic_summary` | Traffic by source |
| `search_console_query` | Custom search analytics query |
| `search_console_top_queries` | Top search queries by clicks |
| `search_console_top_pages` | Top pages by clicks |
| `search_console_summary` | Overall search performance |
| `gtm_list_accounts` | List GTM accounts |
| `gtm_list_containers` | List containers for an account |
| `gtm_container_setup` | Summary of tags/triggers/variables |
| `gtm_list_tags` | List tags in a container |
| `save_insight` | Save a key analytics finding |
| `list_insights` | List all saved insights |
| `delete_insight` | Remove an insight |
| `add_to_watchlist` | Track a page with optional baseline metrics |
| `list_watchlist` | List watched pages |
| `remove_from_watchlist` | Stop tracking a page |
| `save_segment` | Save a reusable filter segment |
| `list_segments` | List saved segments |
| `get_context` | Load all memory at session start |

## REST API Authentication
- All `/api/*` endpoints require `X-API-Key` header when `ANNY_API_KEY` is set
- `GET /health` is unauthenticated (monitoring)
- MCP endpoints (`/mcp/*`) are unauthenticated (auth at transport layer)
- Set `ANNY_API_KEY=` (empty) to disable auth in development

## REST API Endpoints
- `GET /health` — Health check (no auth)
- `POST /api/ga4/report` — Custom GA4 report
- `GET /api/ga4/top-pages` — Top pages
- `GET /api/ga4/traffic-summary` — Traffic summary
- `POST /api/search-console/query` — Custom SC query
- `GET /api/search-console/top-queries` — Top queries
- `GET /api/search-console/top-pages` — Top pages
- `GET /api/search-console/summary` — Performance summary
- `GET /api/tag-manager/accounts` — GTM accounts
- `GET /api/tag-manager/containers` — GTM containers
- `GET /api/tag-manager/tags` — GTM tags
- `GET /api/tag-manager/triggers` — GTM triggers
- `GET /api/tag-manager/variables` — GTM variables
- `GET /api/tag-manager/container-setup` — Full container overview

## Conventions
- Python: formatted with Black (line-length=100), linted with pylint
- Tests: pytest with pytest-cov (135 tests, 82% coverage)
- Task runner: `make help` for all targets
- FastAPI app in `src/anny/main.py`
- Pre-commit hooks enforce format + lint + test on every commit
- Service layer shared between REST and MCP — never duplicate Google API logic
- Lazy credentials — clients created on first use, not at startup

## Current Status (2026-02-17)
- **Code:** Full implementation. 135 tests, pylint 10/10, 82% coverage.
- **Services:** GA4, Search Console, Tag Manager, Memory — all implemented.
- **MCP:** 21 tools, HTTP at /mcp + stdio entry point.
- **Memory:** JSON file store at `~/.anny/memory.json` — insights, watchlist, segments.
- **Pipeline:** GitHub Actions CI configured.
- **Deployment:** Live at https://anny.membies.com (Vultr VPS, Docker, nginx, TLS).
- **Git:** GitHub repo, branch `main`
