# Bolt 8 — Phase 3 Feature Expansion (2026-02-20)

**Goal:** Add query caching, GA4 realtime reports, Search Console sitemap tools, and data export to expand Anny's analytics capabilities.

## Items

| # | Item | Size | Status | Notes |
|---|------|------|--------|-------|
| 25 | Query cache (in-memory, TTL+LRU) | M | done | Ephemeral cache, not in memory.json |
| 19 | GA4 realtime report tool | M | done | activeUsers, screenPageViews, country dims |
| 20 | Search Console sitemap tools | S | done | List + details (readonly, no submit/delete) |
| 23 | Data export (CSV/JSON download) | S | done | 6 endpoints, BOM-prefixed CSV for Excel |

## Metrics

| Metric | Start | Current |
|--------|-------|---------|
| Version | v0.6.0 | v0.7.0 |
| Tests | 182 | 223 |
| Coverage | 85% | 85% |
| Pylint | 10/10 | 10/10 |
| Deploys | 5 | 5 |
| MCP Tools | 21 | 26 |
| REST Endpoints | 16 | 25 |

## Blockers

| Blocker | Days Open | Notes |
|---------|-----------|-------|
| (none) | | |
