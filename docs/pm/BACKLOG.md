# Anny Product Backlog

> Prioritized by MoSCoW (Must/Should/Could/Won't) within each phase.
> Size: S (< 1hr), M (< half day), L (~ 1 day), XL (multi-day).
> Status: executable | blocked | done

Last groomed: 2026-02-17

---

## Phase 1 — Core Functionality

### Must Have

| # | Item | Size | Status | Notes |
|---|------|------|--------|-------|
| 1 | Project scaffold | M | done | Bolt 1 |
| 2 | GA4 integration (client, service, REST, MCP) | L | done | Bolt 1 |
| 3 | Search Console integration | L | done | Bolt 1 |
| 4 | Tag Manager integration | L | done | Bolt 1 |
| 5 | MCP server (HTTP + stdio) | M | done | Bolt 1 |
| 6 | Service account auth | M | done | Bolt 1 |
| 7 | Error handling + exception hierarchy | S | done | Bolt 1 |

### Should Have

| # | Item | Size | Status | Notes |
|---|------|------|--------|-------|
| 8 | E2e test infrastructure (setup guide, smoke test, pytest e2e) | M | done | Bolt 2 |
| 8a | Validate with real service account credentials | S | done | Bolt 2 — smoke 8/8, e2e 19/19 |
| 9 | Dockerfile + docker-compose | M | done | Bolt 2 |
| 10 | README with setup + usage docs | M | done | Bolt 2 |
| 11 | MCP stdio config for Claude Desktop | S | done | Bolt 2 |

### Could Have

| # | Item | Size | Status | Notes |
|---|------|------|--------|-------|
| 12 | Rate limiting / request throttling | M | executable | Bolt 5 |
| 13 | Structured logging (JSON) | M | executable | Bolt 5 |
| 14 | API key auth for REST endpoints | M | done | Bolt 4 — X-API-Key header, ANNY_API_KEY env var, H-001 closed |

---

## Phase 2 — Deployment & Operations

### Must Have

| # | Item | Size | Status | Notes |
|---|------|------|--------|-------|
| 15 | Cloud deployment (Vultr VPS) | L | done | Bolt 2 — anny.membies.com |
| 16 | CI pipeline update for new deps | S | executable | Returned from Bolt 3 |
| 29 | Fix timing attack in verify_api_key | S | executable | Bolt 5 — use hmac.compare_digest |
| 30 | Add file locking to MemoryStore | S | executable | Bolt 5 — prevent concurrent write data loss |
| 31 | Health check validates dependencies | S | executable | Bolt 5 — creds, config, memory path |
| 32 | Startup config validation (fail fast) | S | executable | Bolt 5 — missing required env vars |
| 33 | Fix bare except Exception in clients + auth | S | executable | Bolt 5 — catch specific Google API exceptions |
| 34 | Scrub credentials from error messages | S | executable | Bolt 5 — prevent secret leakage in logs |
| 35 | Add input bounds to MCP tools | S | executable | Bolt 5 — match REST Pydantic validation |
| 36 | Validate CSV fields in service layer | S | executable | Bolt 5 — no empty metrics/dimensions |
| 37 | Validate custom date ranges in date_utils | S | executable | Bolt 5 — reject invalid dates, enforce order |
| 38 | Move pytest out of pre-commit | S | executable | Bolt 5 — keep format + lint only, tests in CI |

### Should Have

| # | Item | Size | Status | Notes |
|---|------|------|--------|-------|
| 17 | Health check with dependency status | S | done | Superseded by #31 |
| 18 | Monitoring / alerting setup | M | executable | |

---

## Phase 3 — Feature Expansion

### Must Have

| # | Item | Size | Status | Notes |
|---|------|------|--------|-------|
| 24 | Memory layer (MemoryStore + service + 9 MCP tools) | L | done | Bolt 4 — insights, watchlist, segments |
| 25 | Query cache for MemoryStore | M | executable | Bolt 4 — cache API responses to avoid re-querying |

### Could Have

| # | Item | Size | Status | Notes |
|---|------|------|--------|-------|
| 19 | GA4 realtime report tool | M | executable | |
| 20 | Search Console sitemap tools | S | executable | |
| 21 | GTM workspace management (create/publish) | L | executable | Requires write scopes |
| 22 | Multi-property support | M | executable | Query across multiple GA4 properties |
| 23 | Data export (CSV/JSON download) | S | executable | |
| 26 | GA4 key event creation via Admin API | M | blocked | Needs analytics.edit scope + Admin API |
| 27 | Conversion optimization audit tooling | M | executable | Only 9/40+ content pages have CTAs |
| 28 | Social channel reactivation strategy | S | executable | Organic social dropped 92% Q3→Q4 |

---

## Won't Do (Decided Against)

| Item | Reason |
|------|--------|
