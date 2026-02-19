# Sprint Log

Archive of completed Bolts.

---

## Bolt 5 — Production Hardening & Code Quality (2026-02-17 → 2026-02-18)

**Goal:** Fix security vulnerabilities, add operational visibility, and harden error handling across the codebase

**Outcome:** ACHIEVED — All 12 items completed in 2 commits. Timing attack fixed, file locking added, health check enhanced, structured logging throughout, exception handling tightened, input validation hardened, rate limiting added, pre-commit streamlined.

### Items Completed

| Item | Size | Notes |
|------|------|-------|
| Fix timing attack in verify_api_key | S | hmac.compare_digest() for constant-time comparison |
| Add file locking to MemoryStore | S | fcntl.flock() with atomic _modify() pattern |
| Health check validates dependencies | S | Config, credentials file, memory path checks |
| Startup config validation (fail fast) | S | validate_config() with logging warnings |
| Structured logging throughout app | M | logging.getLogger("anny") in all modules |
| Fix bare except Exception in clients + auth | S | GoogleAPICallError (GA4), HttpError (SC/GTM), ValueError/KeyError (auth) |
| Scrub credentials from error messages | S | Generic "invalid key file format" instead of exception details |
| Add input bounds to MCP tools | S | MAX_LIMIT=100, MAX_ROW_LIMIT=1000, clamping in all 5 tools |
| Validate CSV fields in service layer | S | Filter empty strings, raise ValueError on empty metrics/dimensions |
| Validate custom date ranges in date_utils | S | ISO format validation, start <= end enforcement |
| Rate limiting middleware | M | 60 req/min per IP on /api/*, in-memory, 429 response |
| Move pytest out of pre-commit | S | Keep black + pylint only, tests via make test + CI |

### Items Not Completed (Returned to Backlog)

(none — all items completed)

### Metrics

| Metric | Value |
|--------|-------|
| Commits | 7 |
| Tests | 164 collected / 145 unit+int passing / 19 e2e |
| Coverage | 83% |
| Pylint | 10/10 |
| Deploys | 1 (v0.4.0 to anny.membies.com) |
| MCP Tools | 21 |

### Retro

- **Went well:** Clean sweep — all 12 items done. Priority ordering (critical → high → medium → low) kept focus. Each fix was small and self-contained.
- **Improve:** Should deploy the hardened code before closing the Bolt to validate in production.
- **Action:** Deploy hardened build to anny.membies.com as first action in next session.

---

## Bolt 4 — Analytics Intelligence (2026-02-17 → 2026-02-17)

**Goal:** Build memory and caching layer so Anny retains insights, watchlists, and query results across sessions

**Outcome:** ACHIEVED — Memory layer delivered with full test coverage. API key auth pulled from backlog and completed as bonus (H-001 closed). Query cache deferred to backlog. Codebase audit identified 12 hardening items, triggering Bolt 5.

### Items Completed

| Item | Size | Notes |
|------|------|-------|
| Memory layer — MemoryStore client + service + 9 MCP tools | L | JSON file store at ~/.anny/memory.json |
| Memory layer tests (store, service, tools — 39 tests) | M | 127 unit+int total |
| Deploy script permission fix (chmod 644) | S | Docker UID compatibility |
| Analytics insights audit (16-month deep analysis) | L | Nov 2024–Feb 2026, 56 cached datasets |
| API key auth for all 13 REST endpoints (H-001) | M | X-API-Key header, ANNY_API_KEY env var |
| Auth tests (8 tests) | S | valid/invalid/missing key, override bypass |

### Items Not Completed (Returned to Backlog)

| Item | Size | Notes |
|------|------|-------|
| Query cache for MemoryStore | M | Still executable — deferred to feature phase |

### Metrics

| Metric | Value |
|--------|-------|
| Commits | 5 |
| Tests | 154 collected / 135 unit+int passing / 19 e2e |
| Coverage | 82% |
| Pylint | 10/10 |
| Deploys | 1 (anny.membies.com live) |
| MCP Tools | 21 |

### Retro

- **Went well:** API key auth followed existing dependency injection pattern perfectly. Codebase audit surfaced concrete, actionable items rather than vague concerns.
- **Improve:** Query cache was planned but never started — should have been scoped more tightly or dropped earlier.
- **Action:** Keep Bolt scope to items you'll actually work on. Defer "nice to haves" to backlog immediately.

---

## Bolt 3 — Production Hardening & Ops (2026-02-16 → 2026-02-17)

**Goal:** Harden the deployed service with auth, observability, and CI updates

**Outcome:** PIVOTED — No planned items completed. Session shifted to memory layer implementation, deploy fix, and deep analytics audit. All Bolt 3 items returned to backlog. Opened Bolt 4 with new theme.

### Items Completed (Unplanned)

| Item | Size | Notes |
|------|------|-------|
| Memory layer (MemoryStore + service + 9 MCP tools) | L | JSON file store at ~/.anny/memory.json |
| 39 new tests (store, service, tools) | M | 127 unit+int total |
| Deploy script permission fix | S | chmod 640→644 for Docker UID compat |
| 16-month analytics audit | L | Nov 2024–Feb 2026, cached 56 datasets |
| docs/insights/ directory | M | Audit, strengths, data cache |

### Items Not Completed (Returned to Backlog)

| Item | Size | Notes |
|------|------|-------|
| CI pipeline update for new deps | S | Still executable |
| API key auth for REST endpoints | M | Still executable |
| Health check with dependency status | S | Still executable |
| Rate limiting / request throttling | S | Still executable |

### Metrics

| Metric | Value |
|--------|-------|
| Commits | 0 (work uncommitted) |
| Tests | 146 collected / 127 passing |
| Coverage | ~81% |
| Pylint | 10/10 |
| Deploys | 0 (live fix via SSH) |
| MCP Tools | 12 → 21 |

### Retro

- **Went well:** Memory layer followed existing client/service/MCP pattern perfectly. Analytics audit surfaced actionable insights (paid→organic migration, AI referrals, social collapse).
- **Improve:** Bolt goal didn't match actual work priorities. Should have re-scoped earlier instead of letting unplanned work accumulate.
- **Action:** Be willing to close/pivot Bolts mid-sprint when priorities shift.

---

## Bolt 2 — Live Testing & Deploy (2026-02-14 → 2026-02-16)

**Goal:** Validate with real Google credentials, containerize, and deploy

**Outcome:** ACHIEVED — All items delivered. E2e tests pass against real Google APIs (smoke 8/8, e2e 19/19). Docker containerization complete. Full VPS deployment infrastructure built (Vultr provisioning, server setup, deploy pipeline, SSL automation).

### Items Completed

| Item | Size | Notes |
|------|------|-------|
| Update README with setup instructions | M | Comprehensive docs |
| E2e test infrastructure | M | Setup guide, smoke test, pytest e2e |
| Validate with real service account credentials | S | smoke 8/8, e2e 19/19 |
| Dockerfile + docker-compose | M | Multi-stage build, production hardened |
| MCP stdio config docs | S | Claude Desktop + Claude Code configs |
| Deploy to cloud (Vultr VPS) | L | 4 scripts, 2 nginx configs, Makefile targets |

### Metrics

| Metric | Value |
|--------|-------|
| Commits | 8 |
| Tests | 107 (88 unit/int + 19 e2e) |
| Coverage | 86% |
| Pylint | 10/10 |
| Deploys | 0 (infra ready, first deploy pending) |

### Retro

- **Went well:** Steady progress across sessions. Deploy infra follows proven webengine patterns. Docker-compose hardened for production (localhost binding, log rotation, restart policy).
- **Improve:** First actual deploy not yet executed — infra is built but untested against real VPS.
- **Action:** Execute first deploy early in Bolt 3 to validate the pipeline.

---

## Bolt 1 — Project Setup (2026-02-13 → 2026-02-14)

**Goal:** Initial scaffold and first working endpoint

**Outcome:** ACHIEVED — Exceeded goal. Delivered full conversational analytics tool with GA4, Search Console, and GTM integrations via REST API + MCP server.

### Items Completed

| Item | Size | Notes |
|------|------|-------|
| Project scaffold | M | FastAPI + pyproject + CI + pre-commit |
| Health check endpoint | S | GET /health |
| CI pipeline | S | GitHub Actions |
| Pre-commit hooks | S | Black + pylint + pytest |

### Unplanned Work Delivered

| Item | Size | Notes |
|------|------|-------|
| GA4 integration | L | Client, service, 3 REST endpoints, 3 MCP tools |
| Search Console integration | L | Client, service, 4 REST endpoints, 4 MCP tools |
| Tag Manager integration | L | Client, service, 6 REST endpoints, 4 MCP tools |
| MCP server | M | FastMCP 2.x, HTTP + stdio, 12 tools |
| Auth + config layer | M | Service account, pydantic-settings |
| Error handling | S | Exception hierarchy + HTTP status mapping |
| 88 tests | L | 77 unit + 11 integration, 86% coverage |

### Metrics

| Metric | Value |
|--------|-------|
| Commits | 4 |
| Tests | 88 |
| Coverage | 86% |
| Pylint | 10/10 |
| Deploys | 0 |

### Retro

- **Went well:** Massive feature delivery in a single session. Clean architecture with shared service layer.
- **Improve:** Need to track unplanned work in Bolts as it happens. Backlog wasn't updated during implementation.
- **Action:** Keep backlog groomed during implementation sessions, not just at PM checkpoints.
