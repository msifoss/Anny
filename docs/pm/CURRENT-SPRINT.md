# Bolt 7 — Monitoring, Alerting & Centralized Logging (2026-02-20)

**Goal:** Add structured JSON logging, Sentry error tracking, admin logs endpoint, and uptime monitoring.

**Tickets:** #18 (Monitoring/alerting setup), #44 (Centralized logging)

## Deliverables

| Item | Size | Status | Notes |
|------|------|--------|-------|
| Structured JSON logging (`core/logging.py`) | M | done | python-json-logger, request-ID via contextvars, ring buffer handler |
| Request-ID middleware | S | done | UUID per request, X-Request-ID response header |
| Request logging middleware | S | done | Method, path, status, duration_ms, client_ip; skips /health |
| Sentry integration | S | done | sentry-sdk[fastapi], init only when SENTRY_DSN set |
| Admin logs endpoint (`GET /api/logs`) | S | done | Ring buffer query, limit/level params, auth-protected |
| Uptime monitor script | S | done | Cron-based, state tracking, webhook alerting |
| Deploy script smoke test | S | done | Post-deploy smoke_test.sh integration |
| Tests (26 new) | M | done | test_logging, test_logs_routes, test_request_middleware, test_sentry_init |

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| Version | v0.5.0 | v0.6.0 |
| Tests | 156 unit+int | 182 unit+int |
| Coverage | 84% | 85% |
| Pylint | 10/10 | 10/10 |
| MCP Tools | 21 | 21 |

## Blockers

| Blocker | Days Open | Notes |
|---------|-----------|-------|
| (none) | | |
