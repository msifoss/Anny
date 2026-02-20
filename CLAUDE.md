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
├── .pre-commit-config.yaml      # Format + lint on every commit
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
│       │   ├── cache_routes.py  # Cache admin endpoints
│       │   ├── export_routes.py # CSV/JSON data export endpoints
│       │   ├── ga4_routes.py    # GA4 REST endpoints
│       │   ├── logs_routes.py    # Admin logs endpoint
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
│           ├── cache.py         # QueryCache (in-memory, TTL+LRU)
│           ├── config.py        # Settings(BaseSettings) from env
│           ├── date_utils.py    # Named date range parsing
│           ├── dependencies.py  # Lazy singleton client factories
│           ├── exceptions.py    # AnnyError, AuthError, APIError
│           ├── formatting.py    # Text table formatting for MCP
│           ├── logging.py       # JSON logging, request-ID, ring buffer
│           └── services/
│               ├── __init__.py
│               ├── cache_service.py
│               ├── export_service.py
│               ├── ga4_service.py
│               ├── memory_service.py
│               ├── search_console_service.py
│               └── tag_manager_service.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/                    # 219 unit tests
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
| `ga4_realtime` | Realtime active users and metrics |
| `search_console_query` | Custom search analytics query |
| `search_console_top_queries` | Top search queries by clicks |
| `search_console_top_pages` | Top pages by clicks |
| `search_console_summary` | Overall search performance |
| `search_console_sitemaps` | List submitted sitemaps |
| `search_console_sitemap_details` | Details for a specific sitemap |
| `cache_status` | Query cache status (entries, TTL) |
| `clear_cache` | Clear all cached query results |
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

## Authentication
- All `/api/*` REST endpoints require `X-API-Key` header when `ANNY_API_KEY` is set
- MCP HTTP (`/mcp`) requires `Authorization: Bearer <ANNY_API_KEY>` when key is set
- Both REST and MCP validate against the same `ANNY_API_KEY` env var
- `GET /health` is unauthenticated (monitoring)
- MCP stdio transport has no auth (runs locally)
- Set `ANNY_API_KEY=` (empty) to disable all auth in development

## REST API Endpoints
- `GET /health` — Health check (no auth)
- `POST /api/ga4/report` — Custom GA4 report
- `GET /api/ga4/top-pages` — Top pages
- `GET /api/ga4/traffic-summary` — Traffic summary
- `GET /api/ga4/realtime` — Realtime active users
- `POST /api/search-console/query` — Custom SC query
- `GET /api/search-console/top-queries` — Top queries
- `GET /api/search-console/top-pages` — Top pages
- `GET /api/search-console/summary` — Performance summary
- `GET /api/search-console/sitemaps` — List sitemaps
- `GET /api/search-console/sitemaps/{feedpath}` — Sitemap details
- `GET /api/tag-manager/accounts` — GTM accounts
- `GET /api/tag-manager/containers` — GTM containers
- `GET /api/tag-manager/tags` — GTM tags
- `GET /api/tag-manager/triggers` — GTM triggers
- `GET /api/tag-manager/variables` — GTM variables
- `GET /api/tag-manager/container-setup` — Full container overview
- `GET /api/logs` — Recent log entries (admin, auth required)
- `GET /api/cache/status` — Cache status (entries, TTL)
- `DELETE /api/cache` — Clear query cache
- `GET /api/export/ga4/report` — Export GA4 report (CSV/JSON)
- `GET /api/export/ga4/top-pages` — Export top pages (CSV/JSON)
- `GET /api/export/ga4/traffic-summary` — Export traffic summary (CSV/JSON)
- `GET /api/export/search-console/query` — Export SC query (CSV/JSON)
- `GET /api/export/search-console/top-queries` — Export top queries (CSV/JSON)
- `GET /api/export/search-console/top-pages` — Export SC top pages (CSV/JSON)

## Conventions
- Python: formatted with Black (line-length=100), linted with pylint
- Tests: pytest with pytest-cov (230 tests, 85% coverage)
- Task runner: `make help` for all targets
- FastAPI app in `src/anny/main.py`
- Pre-commit hooks enforce format + lint on every commit (tests via `make test` + CI)
- Service layer shared between REST and MCP — never duplicate Google API logic
- Lazy credentials — clients created on first use, not at startup

## Current Status (2026-02-20)
- **Code:** Full implementation. 230 tests, pylint 10/10, 85% coverage.
- **Services:** GA4 (incl. realtime), Search Console (incl. sitemaps), Tag Manager, Memory, Cache, Export — all implemented.
- **Cache:** In-memory query cache with TTL (3600s) and LRU eviction (500 entries). Wired into GA4 and SC services.
- **Export:** CSV and JSON download for GA4 and SC reports (6 endpoints with Content-Disposition headers, CSV injection protection, limit clamping).
- **Observability:** Structured JSON logging, request-ID tracking, Sentry error tracking (optional), admin logs endpoint, uptime monitor script.
- **Security:** API key auth (REST X-API-Key + MCP Bearer token), timing-safe comparison, credential scrubbing, rate limiting (60 req/min).
- **MCP:** 26 tools, HTTP at /mcp (Bearer auth) + stdio entry point.
- **Memory:** JSON file store at `~/.anny/memory.json` — insights, watchlist, segments. File-locked for concurrency.
- **OPS Readiness:** 42/47 (89%). Incident response runbook, DR plan (backup + RTO/RPO), automated rollback on failed deploy.
- **Pipeline:** GitHub Actions CI configured.
- **Deployment:** Live at https://anny.membies.com (Vultr VPS, Docker, nginx, TLS). Automated rollback on failed deploy.
- **Git:** GitHub repo, branch `main`
