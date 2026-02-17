# Anny Product Backlog

> Prioritized by MoSCoW (Must/Should/Could/Won't) within each phase.
> Size: S (< 1hr), M (< half day), L (~ 1 day), XL (multi-day).
> Status: executable | blocked | done

Last groomed: 2026-02-16

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
| 12 | Rate limiting / request throttling | S | executable | Bolt 3 |
| 13 | Structured logging (JSON) | S | executable | |
| 14 | API key auth for REST endpoints | M | executable | Bolt 3 |

---

## Phase 2 — Deployment & Operations

### Must Have

| # | Item | Size | Status | Notes |
|---|------|------|--------|-------|
| 15 | Cloud deployment (Vultr VPS) | L | done | Bolt 2 — anny.membies.com |
| 16 | CI pipeline update for new deps | S | executable | Bolt 3 |

### Should Have

| # | Item | Size | Status | Notes |
|---|------|------|--------|-------|
| 17 | Health check with dependency status | S | executable | Bolt 3 — check Google API connectivity |
| 18 | Monitoring / alerting setup | M | executable | |

---

## Phase 3 — Feature Expansion

### Could Have

| # | Item | Size | Status | Notes |
|---|------|------|--------|-------|
| 19 | GA4 realtime report tool | M | executable | |
| 20 | Search Console sitemap tools | S | executable | |
| 21 | GTM workspace management (create/publish) | L | executable | Requires write scopes |
| 22 | Multi-property support | M | executable | Query across multiple GA4 properties |
| 23 | Data export (CSV/JSON download) | S | executable | |

---

## Won't Do (Decided Against)

| Item | Reason |
|------|--------|
