# Anny Product Backlog

> Prioritized by MoSCoW (Must/Should/Could/Won't) within each phase.
> Size: S (< 1hr), M (< half day), L (~ 1 day), XL (multi-day).
> Status: executable | blocked | done

Last groomed: 2026-02-21

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
| 12 | Rate limiting / request throttling | M | done | Bolt 5 — 60 req/min per IP, in-memory |
| 13 | Structured logging | M | done | Bolt 5 — logging.getLogger("anny") throughout |
| 14 | API key auth for REST endpoints | M | done | Bolt 4 — X-API-Key header, ANNY_API_KEY env var, H-001 closed |

---

## Phase 2 — Deployment & Operations

### Must Have

| # | Item | Size | Status | Notes |
|---|------|------|--------|-------|
| 15 | Cloud deployment (Vultr VPS) | L | done | Bolt 2 — anny.membies.com |
| 16 | CI pipeline update for new deps | S | done | Pip cache, coverage gate 80%, pylint gate 9.5, dev deps pinned |
| 29 | Fix timing attack in verify_api_key | S | done | Bolt 5 — hmac.compare_digest |
| 30 | Add file locking to MemoryStore | S | done | Bolt 5 — fcntl.flock + atomic _modify() |
| 31 | Health check validates dependencies | S | done | Bolt 5 — config, creds, memory checks |
| 32 | Startup config validation (fail fast) | S | done | Bolt 5 — validate_config() + logging |
| 33 | Fix bare except Exception in clients + auth | S | done | Bolt 5 — GoogleAPICallError, HttpError |
| 34 | Scrub credentials from error messages | S | done | Bolt 5 — generic error strings |
| 35 | Add input bounds to MCP tools | S | done | Bolt 5 — MAX_LIMIT=100, MAX_ROW_LIMIT=1000 |
| 36 | Validate CSV fields in service layer | S | done | Bolt 5 — reject empty metrics/dimensions |
| 37 | Validate custom date ranges in date_utils | S | done | Bolt 5 — format + order validation |
| 38 | Move pytest out of pre-commit | S | done | Bolt 5 — black + pylint only |
| 39 | MCP HTTP Bearer token auth | M | done | Bolt 6 — DebugTokenVerifier + verify_mcp_bearer_token() |
| 41 | Security audit round 2 fixes (10 items) | M | done | Bolt 6 — H-001, M-001–M-005, L-001–L-002, L-004 |
| 42 | Gitleaks pre-commit secret scanning | S | done | Bolt 6 — v8.24.0, language: golang |
| 43 | Pin all dependency versions | S | done | Bolt 6 — 8 deps pinned to exact versions |

### Should Have

| # | Item | Size | Status | Notes |
|---|------|------|--------|-------|
| 17 | Health check with dependency status | S | done | Superseded by #31 |
| 18 | Monitoring / alerting setup | M | executable | |
| 40 | Docker volume for memory.json persistence | S | done | Named volume + Dockerfile mkdir, deployed |
| 44 | Centralized logging (M-006) | M | executable | Log shipping + alerting — deferred from Bolt 6 |

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
