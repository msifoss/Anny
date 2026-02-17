# Anny — Requirements

**Version:** 0.3.0
**Last updated:** 2026-02-17

---

## Functional Requirements

### FR-001: GA4 Analytics Reporting
The system shall query Google Analytics 4 Data API v1beta and return metric/dimension reports for a specified property.

- **FR-001.1:** Custom reports with arbitrary metrics, dimensions, date ranges, and row limits
- **FR-001.2:** Top pages by screen page views (configurable date range and limit)
- **FR-001.3:** Traffic summary by session source (configurable date range)

### FR-002: Search Console Analytics
The system shall query Google Search Console API v1 and return search analytics data for a specified site URL.

- **FR-002.1:** Custom queries with arbitrary dimensions, date ranges, and row limits
- **FR-002.2:** Top search queries by clicks (configurable date range and limit)
- **FR-002.3:** Top pages by clicks (configurable date range and limit)
- **FR-002.4:** Overall performance summary (clicks, impressions, CTR, position)

### FR-003: Tag Manager Read Access
The system shall query Google Tag Manager API v2 and return account, container, tag, trigger, and variable data.

- **FR-003.1:** List all GTM accounts accessible to the service account
- **FR-003.2:** List containers for a given account
- **FR-003.3:** List tags in a container workspace
- **FR-003.4:** List triggers in a container workspace
- **FR-003.5:** List variables in a container workspace
- **FR-003.6:** Container setup summary (tags + triggers + variables with counts)

### FR-004: MCP Server
The system shall expose all analytics functionality as MCP (Model Context Protocol) tools consumable by LLM clients.

- **FR-004.1:** Health check tool (ping)
- **FR-004.2:** GA4 tools (report, top_pages, traffic_summary)
- **FR-004.3:** Search Console tools (query, top_queries, top_pages, summary)
- **FR-004.4:** Tag Manager tools (list_accounts, list_containers, container_setup, list_tags)
- **FR-004.5:** MCP over HTTP at `/mcp` endpoint
- **FR-004.6:** MCP over stdio for CLI/desktop integration

### FR-005: REST API
The system shall expose all analytics functionality as REST API endpoints.

- **FR-005.1:** GA4 endpoints at `/api/ga4/` (report, top-pages, traffic-summary)
- **FR-005.2:** Search Console endpoints at `/api/search-console/` (query, top-queries, top-pages, summary)
- **FR-005.3:** Tag Manager endpoints at `/api/tag-manager/` (accounts, containers, tags, triggers, variables, container-setup)
- **FR-005.4:** Health check at `GET /health`

### FR-006: Memory Layer
The system shall persist analytics insights, watchlist items, and filter segments to a local JSON file.

- **FR-006.1:** Save, list, and delete insights (text, source, tags)
- **FR-006.2:** Add, list, and remove watchlist items (page path, label, baseline metrics)
- **FR-006.3:** Save, list, and delete filter segments (name, description, filter type, patterns)
- **FR-006.4:** Load all memory context for session initialization
- **FR-006.5:** All memory operations exposed as MCP tools

### FR-007: Date Range Parsing
The system shall accept named date ranges (last_7_days, last_28_days, etc.) and explicit date pairs (YYYY-MM-DD).

### FR-008: Shared Service Layer
REST and MCP interfaces shall share a single service layer with zero duplication of Google API logic.

---

## Non-Functional Requirements

### NFR-001: Authentication
The system shall authenticate to Google APIs using a single service account with readonly scopes only.

### NFR-002: Lazy Initialization
API clients shall be created lazily on first use (not at application startup) and cached as singletons.

### NFR-003: Error Handling
All Google API errors shall be caught and mapped to appropriate error types (AuthError → 401, APIError → 502, AnnyError → 500).

### NFR-004: Code Quality
- Python 3.12+, formatted with Black (line-length 100), linted with pylint (score 10/10)
- Pre-commit hooks enforce format + lint + test on every commit

### NFR-005: Test Coverage
- Minimum 80% code coverage
- Unit tests for all clients, services, and MCP tool formatting
- Integration tests for full REST stack with mocked Google responses
- E2e tests against real Google APIs (gated behind ANNY_E2E=1)

### NFR-006: Containerization
The system shall be deployable as a Docker container with multi-stage builds, non-root user, and health checks.

### NFR-007: CI Pipeline
GitHub Actions shall run format-check, lint, unit+integration tests, and dependency audit on every push/PR to main.

### NFR-008: MCP Tool Output
All MCP tools shall return human-readable text tables formatted via `format_table()`.

---

## Security Requirements

### SEC-001: Readonly Scopes
All Google API authentication scopes shall be readonly. No write access to GA4, Search Console, or GTM.

### SEC-002: Secret Management
Service account key files shall never be committed to version control. `.gitignore` shall exclude all `*.json` key patterns.

### SEC-003: HTTPS Enforcement
Production deployment shall enforce HTTPS with TLS 1.2+ and HSTS headers.

### SEC-004: Container Security
Docker container shall run as non-root user (UID 1000). Ports shall bind to localhost only in docker-compose.

### SEC-005: Security Headers
Production nginx shall set X-Frame-Options, X-Content-Type-Options, Referrer-Policy, and Permissions-Policy headers.

### SEC-006: Network Security
Production VPS shall use UFW firewall (22/80/443 only) and fail2ban for SSH brute-force protection.

### SEC-007: Dependency Auditing
`pip-audit` shall run in CI pipeline and be available via `make audit` locally.

### SEC-008: Input Validation
All REST request bodies shall be validated via Pydantic models. FastAPI handles automatic request validation.

### SEC-009: Memory Store Security
The memory store JSON file shall be stored in the user's home directory with standard file permissions. No sensitive credentials shall be stored in the memory file.
