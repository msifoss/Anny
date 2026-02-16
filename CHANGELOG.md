# Changelog

All notable changes to Anny are documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [Unreleased]

### Added
- Docker containerization: multi-stage `Dockerfile`, `docker-compose.yml`, `.dockerignore`
- `make docker-build` and `make docker-run` targets
- Service account setup guide (`docs/manuals/SERVICE-ACCOUNT-SETUP.md`)
- Smoke test script (`scripts/smoke_test.sh`) — curl-based endpoint validation with color-coded output
- 19 e2e tests (GA4, Search Console, Tag Manager, health) gated behind `ANNY_E2E=1`
- `make e2e` and `make smoke` targets
- `e2e` pytest marker registration
- `.gitignore` patterns for service account JSON key files

### Changed
- `.env.example` trimmed to only the 3 fields accepted by Settings (removed APP_NAME, APP_ENV, etc.)
- CI pipeline narrowed to `tests/unit/` and `tests/integration/` (skips e2e collection)

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
