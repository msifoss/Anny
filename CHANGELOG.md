# Changelog

All notable changes to Anny are documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [Unreleased]

## [0.4.0] - 2026-02-18 (Security Hardening + Production Auth)

### Added
- API key authentication for all 13 REST endpoints via `X-API-Key` header
- `ANNY_API_KEY` environment variable in Settings (empty = auth disabled)
- `verify_api_key` dependency in `dependencies.py` using FastAPI `APIKeyHeader`
- Constant-time API key comparison via `hmac.compare_digest()` (timing attack fix)
- File locking in MemoryStore with `fcntl.flock()` and atomic `_modify()` pattern
- Enhanced health check: validates config, credentials file, memory path writability
- Startup config validation with `validate_config()` logging warnings for missing settings
- Structured logging via `logging.getLogger("anny")` across all modules
- Rate limiting middleware: 60 requests/minute per IP on `/api/*` endpoints (429 response)
- Custom date range validation: ISO format check, start <= end enforcement
- CSV field validation: reject empty metrics/dimensions in service layer
- Input bounds clamping in MCP tools (`MAX_LIMIT=100`, `MAX_ROW_LIMIT=1000`)
- `ANNY_API_KEY` passed to Docker container via `docker-compose.yml`
- 18 new tests (145 unit+int total, 164 collected)

### Changed
- Exception handling: `except Exception` replaced with specific types (`GoogleAPICallError`, `HttpError`, `ValueError`/`KeyError`)
- Credential error messages scrubbed — generic "invalid key file format" instead of exception details
- Pre-commit hooks streamlined: removed pytest (kept black + pylint), tests run via `make test` + CI
- Route tests refactored to properly override `verify_api_key` (fixes failures when `ANNY_API_KEY` is set)
- SECURITY.md: H-001 (unauthenticated REST API) resolved, M-001 (rate limiting) resolved
- `.env.example`: added `ANNY_API_KEY=` entry

## [0.3.0] - 2026-02-17 (Memory Layer + Deployment + Compliance)

### Added
- Memory layer: `MemoryStore` client, `memory_service`, 9 MCP tools (save/list/delete insights, watchlist, segments + get_context)
- `~/.anny/memory.json` persistent store with sortable ID generation
- `get_memory_store()` lazy singleton in dependencies
- 39 new tests (14 store, 15 service, 10 tools) — 127 unit+int total
- `docs/insights/` directory with analytics audit, positioning strengths, and cached API data
- 16-month analytics audit (Nov 2024–Feb 2026) with quarter-by-quarter analysis
- Vultr VPS deployment infrastructure for anny.membies.com
- Server provisioning script (`scripts/server-provision.sh`) — Vultr API, DNS A record
- Server setup script (`scripts/server-setup.sh`) — Docker, nginx, UFW, fail2ban, deploy user
- Deploy script (`scripts/deploy.sh`) — rsync, secrets upload, container build, health check
- SSL setup script (`scripts/ssl-setup.sh`) — certbot, HTTPS nginx config
- Nginx configs: `deploy/nginx-http.conf` (pre-SSL), `deploy/nginx-https.conf` (post-SSL)
- `make provision`, `make setup`, `make deploy`, `make ssl-setup` targets
- MCP stdio setup guide (`docs/manuals/MCP-STDIO-SETUP.md`) — Claude Desktop, Claude Code, Docker configs
- Docker containerization: multi-stage `Dockerfile`, `docker-compose.yml`, `.dockerignore`
- `make docker-build` and `make docker-run` targets
- Service account setup guide (`docs/manuals/SERVICE-ACCOUNT-SETUP.md`)
- Smoke test script (`scripts/smoke_test.sh`) — curl-based endpoint validation with color-coded output
- 19 e2e tests (GA4, Search Console, Tag Manager, health) gated behind `ANNY_E2E=1`
- `make e2e` and `make smoke` targets
- `e2e` pytest marker registration
- `.gitignore` patterns for service account JSON key files
- Formal requirements (`docs/REQUIREMENTS.md`) — 8 FR, 8 NFR, 9 SEC requirements
- Traceability matrix (`docs/TRACEABILITY-MATRIX.md`) — requirements mapped to code and tests
- User stories (`docs/USER-STORIES.md`) — 12 stories across 3 personas
- OPS readiness checklist (`docs/standards/OPS-READINESS-CHECKLIST.md`) — 47 items, scored 28/47
- Security audit (`docs/security/security-audit-2026-02-17.md`) — 1 High, 4 Medium, 5 Low
- AI-DLC framework docs (7 standards documents addressing all 10 shortcomings)
- Release runbook (`docs/manuals/RELEASE_RUNBOOK.md`) — doc sync matrix, rollback procedure

### Changed
- `docker-compose.yml` hardened for production: localhost-only port binding, `restart: unless-stopped`, log rotation (10m/3 files), secrets mount path
- `.env.example` trimmed to only the 3 fields accepted by Settings (removed APP_NAME, APP_ENV, etc.)
- CI pipeline narrowed to `tests/unit/` and `tests/integration/` (skips e2e collection)
- Version bumped to 0.3.0 in `pyproject.toml` and `main.py`
- CLAUDE.md updated with deployment status (live at anny.membies.com)
- SECURITY.md updated with audit findings and security controls
- Deploy script fixed: `chmod 640` → `chmod 644` for Docker UID compatibility

## [0.2.0] - 2026-02-13 (Conversational Analytics)

### Added
- Google Analytics 4 integration (GA4Client, service layer, 3 REST endpoints, 3 MCP tools)
- Google Search Console integration (SearchConsoleClient, service layer, 4 REST endpoints, 4 MCP tools)
- Google Tag Manager integration (TagManagerClient, service layer, 6 REST endpoints, 4 MCP tools)
- MCP server (FastMCP 2.x) with 12 tools, mounted at /mcp and available via stdio
- Service account authentication with readonly scopes for GA4, SC, GTM
- Pydantic Settings configuration (GOOGLE_SERVICE_ACCOUNT_KEY_PATH, GA4_PROPERTY_ID, SEARCH_CONSOLE_SITE_URL)
- Custom exception hierarchy (AnnyError, AuthError, APIError) with HTTP status mapping
- Lazy singleton client factories via lru_cache
- Date range parser supporting named ranges (last_7_days, last_28_days, etc.) and explicit dates
- Text table formatter for MCP tool output
- Error handler mapping AnnyError subtypes to HTTP 401/502/500
- `make mcp` target for stdio MCP server
- 88 tests (77 unit + 11 integration), pylint 10/10, 86% coverage

### Changed
- Updated requirements.txt with google-auth, google-analytics-data, google-api-python-client, pydantic-settings, fastmcp
- Updated pyproject.toml with new dependencies and pylint config
- Updated .env.example with Google service account configuration
- Updated CLAUDE.md with full architecture, MCP tools, and REST API documentation

## [0.1.0] - 2026-02-13 (Initial Scaffold)

### Added
- Project directory structure
- CLAUDE.md — AI operating manual
- README.md — comprehensive project documentation
- SECURITY.md — security policy and controls
- CHANGELOG.md — this file
- Makefile with standard targets
- GitHub Actions CI pipeline
- Pre-commit hooks (Black + pylint + pytest)
- PM framework (Bolt-based sprints)
- FastAPI application with health check endpoint
- pyproject.toml with pytest, Black, pylint config
- .gitignore, .env.example, VS Code settings
- docs/ structure (manuals, security, reviews, PM, captain's log)
- Placeholder unit test
