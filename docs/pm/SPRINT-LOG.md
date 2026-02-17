# Sprint Log

Archive of completed Bolts.

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
