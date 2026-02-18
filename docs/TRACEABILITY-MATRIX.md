# Anny — Traceability Matrix

**Last updated:** 2026-02-18
**Test count:** 145 unit+integration, 19 e2e (164 total)

---

## Functional Requirements

| Req ID | Requirement | Source Files | Test Files | Tests |
|--------|------------|-------------|------------|-------|
| FR-001.1 | GA4 custom report | `clients/ga4.py`, `services/ga4_service.py`, `api/ga4_routes.py`, `mcp_server.py` | `test_ga4_client.py`, `test_ga4_service.py`, `test_ga4_tools.py`, `test_ga4_routes.py`, `test_full_stack.py`, `test_ga4_e2e.py` | 14 |
| FR-001.2 | GA4 top pages | `services/ga4_service.py`, `api/ga4_routes.py`, `mcp_server.py` | `test_ga4_service.py`, `test_ga4_tools.py`, `test_ga4_routes.py`, `test_full_stack.py`, `test_ga4_e2e.py` | 6 |
| FR-001.3 | GA4 traffic summary | `services/ga4_service.py`, `api/ga4_routes.py`, `mcp_server.py` | `test_ga4_service.py`, `test_ga4_tools.py`, `test_ga4_routes.py`, `test_full_stack.py`, `test_ga4_e2e.py` | 5 |
| FR-002.1 | SC custom query | `clients/search_console.py`, `services/search_console_service.py`, `api/search_console_routes.py`, `mcp_server.py` | `test_search_console_client.py`, `test_search_console_service.py`, `test_search_console_tools.py`, `test_search_console_routes.py`, `test_full_stack.py`, `test_search_console_e2e.py` | 11 |
| FR-002.2 | SC top queries | `services/search_console_service.py`, `api/search_console_routes.py`, `mcp_server.py` | `test_search_console_service.py`, `test_search_console_tools.py`, `test_search_console_routes.py`, `test_full_stack.py`, `test_search_console_e2e.py` | 5 |
| FR-002.3 | SC top pages | `services/search_console_service.py`, `api/search_console_routes.py`, `mcp_server.py` | `test_search_console_service.py`, `test_search_console_tools.py`, `test_search_console_routes.py`, `test_full_stack.py`, `test_search_console_e2e.py` | 4 |
| FR-002.4 | SC summary | `services/search_console_service.py`, `api/search_console_routes.py`, `mcp_server.py` | `test_search_console_service.py`, `test_search_console_tools.py`, `test_search_console_routes.py`, `test_full_stack.py`, `test_search_console_e2e.py` | 5 |
| FR-003.1 | GTM list accounts | `clients/tag_manager.py`, `services/tag_manager_service.py`, `api/tag_manager_routes.py`, `mcp_server.py` | `test_tag_manager_client.py`, `test_tag_manager_service.py`, `test_tag_manager_tools.py`, `test_tag_manager_routes.py`, `test_full_stack.py`, `test_tag_manager_e2e.py` | 7 |
| FR-003.2 | GTM list containers | `clients/tag_manager.py`, `services/tag_manager_service.py`, `api/tag_manager_routes.py`, `mcp_server.py` | Same as above | 5 |
| FR-003.3 | GTM list tags | `clients/tag_manager.py`, `api/tag_manager_routes.py`, `mcp_server.py` | Same as above | 4 |
| FR-003.4 | GTM list triggers | `clients/tag_manager.py`, `api/tag_manager_routes.py` | `test_tag_manager_client.py`, `test_tag_manager_routes.py` | 2 |
| FR-003.5 | GTM list variables | `clients/tag_manager.py`, `api/tag_manager_routes.py` | `test_tag_manager_client.py`, `test_tag_manager_routes.py` | 2 |
| FR-003.6 | GTM container setup | `services/tag_manager_service.py`, `api/tag_manager_routes.py`, `mcp_server.py` | `test_tag_manager_service.py`, `test_tag_manager_routes.py`, `test_full_stack.py`, `test_tag_manager_e2e.py` | 4 |
| FR-004 | MCP server (all tools) | `mcp_server.py` | `test_ga4_tools.py`, `test_search_console_tools.py`, `test_tag_manager_tools.py`, `test_memory_tools.py` | 20 |
| FR-005 | REST API (all endpoints) | `api/ga4_routes.py`, `api/search_console_routes.py`, `api/tag_manager_routes.py` | `test_ga4_routes.py`, `test_search_console_routes.py`, `test_tag_manager_routes.py`, `test_full_stack.py` | 24 |
| FR-005.4 | Health check | `main.py` | `test_main.py`, `test_full_stack.py`, `test_health_e2e.py` | 3 |
| FR-006.1 | Memory insights | `clients/memory.py`, `services/memory_service.py`, `mcp_server.py` | `test_memory_store.py`, `test_memory_service.py`, `test_memory_tools.py` | 12 |
| FR-006.2 | Memory watchlist | `clients/memory.py`, `services/memory_service.py`, `mcp_server.py` | `test_memory_store.py`, `test_memory_service.py`, `test_memory_tools.py` | 9 |
| FR-006.3 | Memory segments | `clients/memory.py`, `services/memory_service.py`, `mcp_server.py` | `test_memory_store.py`, `test_memory_service.py`, `test_memory_tools.py` | 8 |
| FR-006.4 | Memory get_context | `services/memory_service.py`, `mcp_server.py` | `test_memory_service.py`, `test_memory_tools.py` | 4 |
| FR-007 | Date range parsing | `core/date_utils.py` | `test_date_utils.py` | 10 |
| FR-008 | Shared service layer | Architecture pattern | `test_full_stack.py` (validates both REST and MCP use same services) | — |

## Cross-Cutting Concerns (new since 0.3.0)

| Feature | Source Files | Test Files | Tests |
|---------|-------------|------------|-------|
| API key authentication | `core/dependencies.py`, `api/*_routes.py` | `test_api_auth.py` | 8 |
| Input validation (CSV, date) | `services/ga4_service.py`, `services/search_console_service.py`, `core/date_utils.py` | `test_ga4_service.py`, `test_search_console_service.py`, `test_date_utils.py` | 6 |
| Health check (enhanced) | `main.py` | `test_main.py` | 2 |
| Config validation | `core/config.py` | `test_config.py` | 3 |

## Non-Functional Requirements

| Req ID | Requirement | Evidence |
|--------|------------|---------|
| NFR-001 | Service account auth (readonly) | `core/auth.py` — SCOPES list, `test_auth.py` |
| NFR-002 | Lazy singleton clients | `core/dependencies.py` — `@functools.lru_cache` on all 5 factory functions |
| NFR-003 | Error handling | `core/exceptions.py`, `api/error_handlers.py`, `test_error_handlers.py` — specific exception types (GoogleAPICallError, HttpError) |
| NFR-004 | Code quality (Black + pylint) | `.pre-commit-config.yaml` (format + lint), `.github/workflows/ci.yml`, `pyproject.toml` |
| NFR-005 | Test coverage >= 80% | 145 tests, 83% coverage |
| NFR-006 | Docker containerization | `Dockerfile` (multi-stage, non-root), `docker-compose.yml` |
| NFR-007 | CI pipeline | `.github/workflows/ci.yml` (format, lint, test, audit) |
| NFR-008 | MCP text table output | `core/formatting.py`, `test_formatting.py` |

## Security Requirements

| Req ID | Requirement | Evidence |
|--------|------------|---------|
| SEC-001 | Readonly scopes | `core/auth.py` — `.readonly` in all 3 SCOPES |
| SEC-002 | Secret exclusion | `.gitignore` — `*service-account*.json` patterns |
| SEC-003 | HTTPS enforcement | `deploy/nginx-https.conf` — TLS 1.2+, HSTS, 301 redirect |
| SEC-004 | Non-root container | `Dockerfile` — `USER anny` (UID 1000), `docker-compose.yml` — `127.0.0.1:8000` |
| SEC-005 | Security headers | `deploy/nginx-https.conf` — X-Frame-Options, X-Content-Type-Options, etc. |
| SEC-006 | Network security | `scripts/server-setup.sh` — UFW + fail2ban |
| SEC-007 | Dependency audit | `.github/workflows/ci.yml` — `pip-audit`, `Makefile` — `make audit` |
| SEC-008 | Input validation | `api/models.py` — Pydantic BaseModel; service layer CSV/date validation |
| SEC-009 | Memory store security | `clients/memory.py` — file in `~/.anny/`, fcntl file locking, no credentials stored |
