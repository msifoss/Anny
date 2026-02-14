# Anny

**Conversational analytics for Google Analytics 4, Search Console, and Tag Manager.**

Anny gives LLMs and programmatic clients unified access to your Google analytics stack through two interfaces: a REST API and an MCP server. Point Claude, ChatGPT, or any MCP-compatible agent at Anny and ask questions like "What are my top pages this month?" or "Which search queries are driving traffic?" -- Anny handles the Google API plumbing and returns clean, readable results.

---

## Table of Contents

- [Features](#features)
- [How It Works](#how-it-works)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [REST API](#rest-api)
  - [MCP Server](#mcp-server)
  - [Claude Desktop Integration](#claude-desktop-integration)
- [API Reference](#api-reference)
  - [Google Analytics 4](#google-analytics-4)
  - [Google Search Console](#google-search-console)
  - [Google Tag Manager](#google-tag-manager)
- [MCP Tools Reference](#mcp-tools-reference)
- [Architecture](#architecture)
- [Development](#development)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Features

**Three Google services, two access modes, one codebase.**

| Service | What you can do |
|---------|----------------|
| **Google Analytics 4** | Custom reports, top pages, traffic by source |
| **Google Search Console** | Search queries, page performance, CTR and position data |
| **Google Tag Manager** | List accounts, containers, tags, triggers, variables |

**Access modes:**

- **REST API** -- 14 endpoints with Swagger docs, suitable for dashboards, scripts, and integrations
- **MCP Server** -- 12 tools with sensible defaults, designed for natural-language interaction with LLMs

**Developer experience:**

- Single service account for all three APIs (readonly)
- Named date ranges (`last_7_days`, `last_28_days`) -- no date math required
- Lazy credential loading -- the health check works without any Google credentials
- 88 tests, pylint 10/10, 86% coverage
- Pre-commit hooks enforce formatting, linting, and tests

---

## How It Works

```
┌─────────────────┐     ┌──────────────────┐
│  REST API        │     │  MCP Server      │
│  /api/ga4/...   │     │  /mcp (HTTP)     │
│  /api/sc/...    │     │  stdio (CLI)     │
│  /api/gtm/...   │     │                  │
└────────┬────────┘     └────────┬─────────┘
         │                       │
         └───────────┬───────────┘
                     ▼
              Service Layer
         (shared business logic)
                     │
                     ▼
              Client Layer
         (Google API wrappers)
                     │
                     ▼
           Service Account Auth
         (readonly, all 3 APIs)
```

Both interfaces share the same service layer. There is zero duplication of Google API logic -- a bug fix or new feature in the service layer is immediately available through both REST and MCP.

---

## Installation

### Prerequisites

- Python 3.12+
- A Google Cloud service account with access to GA4, Search Console, and/or Tag Manager

### Setup

```bash
git clone https://github.com/msifoss/Anny.git
cd Anny

# Create virtual environment and install everything
make install

# Verify
make test
```

---

## Configuration

### 1. Create a Google Cloud Service Account

1. Go to [Google Cloud Console](https://console.cloud.google.com/) > IAM & Admin > Service Accounts
2. Create a service account (or use an existing one)
3. Grant it the following roles in the relevant products:
   - **GA4:** Viewer role on the GA4 property
   - **Search Console:** Add the service account email as a user in [Search Console](https://search.google.com/search-console/)
   - **Tag Manager:** Viewer role on the GTM account
4. Create a JSON key and download it

### 2. Enable APIs

Enable these APIs in your Google Cloud project:

- Google Analytics Data API
- Google Search Console API
- Tag Manager API

### 3. Set Environment Variables

```bash
cp .env.example .env
```

Edit `.env` with your values:

```bash
# Path to your downloaded service account JSON key
GOOGLE_SERVICE_ACCOUNT_KEY_PATH=/path/to/service-account-key.json

# Your GA4 property ID (find in GA4 Admin > Property Settings)
GA4_PROPERTY_ID=properties/123456789

# Your site URL as registered in Search Console
SEARCH_CONSOLE_SITE_URL=https://example.com
```

All three settings are optional. If you only use GA4, you only need the key path and property ID. The health check and MCP ping work without any credentials.

---

## Usage

### REST API

Start the server:

```bash
make run
```

The API is available at `http://localhost:8000`. Interactive docs are at `http://localhost:8000/docs`.

**Quick examples:**

```bash
# Health check (no credentials needed)
curl http://localhost:8000/health

# Top pages from GA4
curl "http://localhost:8000/api/ga4/top-pages?date_range=last_7_days&limit=5"

# Traffic summary by source
curl "http://localhost:8000/api/ga4/traffic-summary?date_range=last_28_days"

# Top search queries from Search Console
curl "http://localhost:8000/api/search-console/top-queries?limit=10"

# Custom GA4 report
curl -X POST http://localhost:8000/api/ga4/report \
  -H "Content-Type: application/json" \
  -d '{"metrics": "sessions,totalUsers,bounceRate", "dimensions": "date", "date_range": "last_7_days"}'

# List GTM accounts
curl http://localhost:8000/api/tag-manager/accounts

# Full container audit (tags, triggers, variables)
curl "http://localhost:8000/api/tag-manager/container-setup?container_path=accounts/123/containers/456"
```

### MCP Server

Anny's MCP server can run in two modes:

**HTTP mode** (mounted alongside the REST API):

```bash
make run
# MCP is available at http://localhost:8000/mcp
```

**Stdio mode** (for direct use with Claude Desktop or other MCP clients):

```bash
make mcp
```

### Claude Desktop Integration

Add this to your Claude Desktop MCP configuration (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "anny": {
      "command": "/path/to/Anny/.venv/bin/python",
      "args": ["-m", "anny.cli.mcp_stdio"],
      "env": {
        "GOOGLE_SERVICE_ACCOUNT_KEY_PATH": "/path/to/service-account-key.json",
        "GA4_PROPERTY_ID": "properties/123456789",
        "SEARCH_CONSOLE_SITE_URL": "https://example.com"
      }
    }
  }
}
```

Then ask Claude things like:

> "What are my top 10 pages this month?"
>
> "Show me search queries driving traffic to my site"
>
> "What tags are configured in my GTM container?"

---

## API Reference

### Date Ranges

All endpoints that accept a `date_range` parameter support these values:

| Named Range | Period |
|-------------|--------|
| `today` | Today only |
| `yesterday` | Yesterday only |
| `last_7_days` | Past 7 days |
| `last_14_days` | Past 14 days |
| `last_28_days` | Past 28 days (default) |
| `last_30_days` | Past 30 days |
| `last_90_days` | Past 90 days |
| `last_365_days` | Past 365 days |

You can also pass explicit dates: `2024-01-01,2024-01-31`

### Google Analytics 4

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/ga4/report` | Custom report with any metrics/dimensions |
| `GET` | `/api/ga4/top-pages` | Top pages by page views |
| `GET` | `/api/ga4/traffic-summary` | Traffic breakdown by source |

**POST `/api/ga4/report`** -- Custom report:

```json
{
  "metrics": "sessions,totalUsers,screenPageViews",
  "dimensions": "date",
  "date_range": "last_28_days",
  "limit": 10
}
```

Response:

```json
{
  "rows": [
    {"date": "20240101", "sessions": "523", "totalUsers": "412", "screenPageViews": "1847"}
  ],
  "row_count": 1
}
```

**GET `/api/ga4/top-pages`** -- Query params: `date_range`, `limit`

**GET `/api/ga4/traffic-summary`** -- Query params: `date_range`

### Google Search Console

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/search-console/query` | Custom search analytics query |
| `GET` | `/api/search-console/top-queries` | Top search queries by clicks |
| `GET` | `/api/search-console/top-pages` | Top pages by clicks |
| `GET` | `/api/search-console/summary` | Overall performance summary |

**POST `/api/search-console/query`** -- Custom query:

```json
{
  "dimensions": "query,page",
  "date_range": "last_28_days",
  "row_limit": 10
}
```

Response:

```json
{
  "rows": [
    {"query": "python fastapi", "page": "/docs", "clicks": 120, "impressions": 5000, "ctr": 2.4, "position": 5.3}
  ],
  "row_count": 1
}
```

Available dimensions: `query`, `page`, `date`, `country`, `device`

### Google Tag Manager

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/tag-manager/accounts` | List all GTM accounts |
| `GET` | `/api/tag-manager/containers?account_id=123` | List containers for an account |
| `GET` | `/api/tag-manager/tags?container_path=...` | List tags in a container |
| `GET` | `/api/tag-manager/triggers?container_path=...` | List triggers |
| `GET` | `/api/tag-manager/variables?container_path=...` | List variables |
| `GET` | `/api/tag-manager/container-setup?container_path=...` | Full container overview |

Container paths follow the format: `accounts/{accountId}/containers/{containerId}`

---

## MCP Tools Reference

All tools use sensible defaults. Call them with no arguments for quick results, or customize as needed.

| Tool | Parameters | Default Behavior |
|------|-----------|------------------|
| `ping` | (none) | Returns "pong" |
| `ga4_report` | `metrics`, `dimensions`, `date_range`, `limit` | Sessions + users by date, last 28 days |
| `ga4_top_pages` | `date_range`, `limit` | Top 10 pages by views, last 28 days |
| `ga4_traffic_summary` | `date_range` | Traffic by source, last 28 days |
| `search_console_query` | `dimensions`, `date_range`, `row_limit` | Top queries, last 28 days |
| `search_console_top_queries` | `date_range`, `limit` | Top 10 queries by clicks |
| `search_console_top_pages` | `date_range`, `limit` | Top 10 pages by clicks |
| `search_console_summary` | `date_range` | Overall clicks/impressions/CTR/position |
| `gtm_list_accounts` | (none) | All accessible accounts |
| `gtm_list_containers` | `account_id` | Containers for one account |
| `gtm_container_setup` | `container_path` | Tags + triggers + variables summary |
| `gtm_list_tags` | `container_path` | All tags in a container |

MCP tools return formatted text tables optimized for LLM consumption.

---

## Architecture

```
src/anny/
├── main.py                     # FastAPI app, mounts routers + MCP
├── mcp_server.py               # FastMCP instance + 12 tool definitions
├── api/
│   ├── models.py               # Pydantic request/response models
│   ├── error_handlers.py       # AnnyError → HTTP 401/502/500
│   ├── ga4_routes.py           # 3 GA4 endpoints
│   ├── search_console_routes.py # 4 Search Console endpoints
│   └── tag_manager_routes.py   # 6 Tag Manager endpoints
├── clients/
│   ├── ga4.py                  # GA4Client — wraps BetaAnalyticsDataClient
│   ├── search_console.py       # SearchConsoleClient — wraps searchanalytics API
│   └── tag_manager.py          # TagManagerClient — wraps GTM API v2
├── cli/
│   └── mcp_stdio.py            # Standalone stdio entry point
└── core/
    ├── auth.py                 # Service account credential loading
    ├── config.py               # Pydantic Settings from env vars
    ├── date_utils.py           # Named date range → (start, end) parsing
    ├── dependencies.py         # Lazy singleton client factories (lru_cache)
    ├── exceptions.py           # AnnyError → AuthError, APIError
    ├── formatting.py           # Text table formatter for MCP output
    └── services/
        ├── ga4_service.py
        ├── search_console_service.py
        └── tag_manager_service.py
```

**Key design decisions:**

- **Shared service layer** -- REST routes and MCP tools call the same service functions. No logic duplication.
- **Lazy credentials** -- Google clients are created on first use via `lru_cache`. The app starts and serves `/health` without any credentials configured.
- **Flat MCP parameters** -- MCP tools use simple string parameters (`metrics="sessions,totalUsers"`) rather than complex objects, making them easy for LLMs to call.
- **FastMCP 2.x** -- Decorator-based tool registration with auto-generated schemas from type hints and docstrings.

---

## Development

### Quick Reference

```bash
make help            # Show all available targets
make install         # Create venv, install deps, set up pre-commit hooks
make run             # Start dev server (http://localhost:8000)
make mcp             # Start MCP stdio server
make test            # Run all tests with coverage
make unit            # Run unit tests only
make integration     # Run integration tests only
make lint            # Run pylint
make format          # Format with Black
make format-check    # Check formatting (CI-friendly)
make audit           # Run pip-audit for vulnerabilities
make clean           # Remove build artifacts
```

### Code Quality

Pre-commit hooks run automatically on every commit:

1. **Black** -- Code formatting (line length 100)
2. **pylint** -- Linting (10/10 score enforced)
3. **pytest** -- Tests must pass

---

## Testing

```bash
# Full suite with coverage
make test

# Unit tests only (fast, no I/O)
make unit

# Integration tests only (full request flow with mocked Google APIs)
make integration
```

**Test breakdown:**

| Category | Count | What's tested |
|----------|-------|---------------|
| Unit | 77 | Clients, services, routes, config, auth, date parsing, formatting, exceptions, error handlers |
| Integration | 11 | Full HTTP request flow through FastAPI with mocked Google API responses |
| **Total** | **88** | **86% code coverage** |

All tests use mocked Google API responses -- no real credentials needed to run the test suite.

---

## Troubleshooting

### "GOOGLE_SERVICE_ACCOUNT_KEY_PATH is not set"

You're calling an analytics endpoint without configuring credentials. Set the path in `.env`:

```bash
GOOGLE_SERVICE_ACCOUNT_KEY_PATH=/absolute/path/to/key.json
```

### "Service account key file not found"

The path in `GOOGLE_SERVICE_ACCOUNT_KEY_PATH` doesn't point to an existing file. Verify:

```bash
ls -la /path/to/your/key.json
```

### "GA4 report failed" / "Search Console query failed"

The Google API returned an error. Common causes:

- The service account doesn't have access to the property/site
- The API isn't enabled in your Google Cloud project
- The property ID or site URL is wrong

### Health check works but API endpoints return 401

This is by design. The health check doesn't require credentials. Configure your `.env` file to use the analytics endpoints.

### MCP tools not showing up in Claude Desktop

1. Verify the path to your Python venv is correct in `claude_desktop_config.json`
2. Make sure environment variables are set in the `env` block
3. Restart Claude Desktop after config changes

---

## Contributing

1. Create a feature branch from `main`
2. Make your changes
3. Run the quality checks:

```bash
make format-check && make lint && make test
```

4. Submit a pull request

Pre-commit hooks enforce formatting, linting, and tests automatically on every commit.

---

## License

MIT -- see [LICENSE](LICENSE) for details.
