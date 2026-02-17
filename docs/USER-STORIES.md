# Anny — User Stories

**Last updated:** 2026-02-17

---

## Personas

- **Analyst (LLM):** An AI assistant (Claude, ChatGPT) using MCP tools to answer analytics questions conversationally
- **Developer:** A human building or extending Anny's capabilities
- **Marketer:** A human using REST API or LLM to get analytics insights for business decisions

---

## Stories

### Analytics Queries

**US-001:** As an Analyst, I want to query GA4 for top pages by page views so I can identify which content performs best.
- Acceptance: `ga4_top_pages` MCP tool returns formatted table with page paths and view counts

**US-002:** As an Analyst, I want to query Search Console for top queries so I can understand what people search for to find the site.
- Acceptance: `search_console_top_queries` returns queries sorted by clicks

**US-003:** As an Analyst, I want to run custom GA4 reports with arbitrary metrics and dimensions so I can answer ad-hoc analytics questions.
- Acceptance: `ga4_report` accepts any valid GA4 metric/dimension combination

**US-004:** As a Marketer, I want to see traffic by source/medium so I can evaluate channel performance.
- Acceptance: `ga4_traffic_summary` or `GET /api/ga4/traffic-summary` returns source breakdown

**US-005:** As an Analyst, I want to see GTM container configuration so I can audit tracking implementation.
- Acceptance: `gtm_container_setup` returns tags, triggers, and variables with counts

### Memory & Context

**US-006:** As an Analyst, I want to save key findings so I can reference them in future sessions without re-querying.
- Acceptance: `save_insight` persists to `~/.anny/memory.json`, `list_insights` retrieves them

**US-007:** As an Analyst, I want to track specific pages over time so I can monitor performance changes.
- Acceptance: `add_to_watchlist` saves page path with optional baseline metrics

**US-008:** As an Analyst, I want to save reusable filter segments so I can apply consistent exclusions across queries.
- Acceptance: `save_segment` persists filter patterns, retrievable via `list_segments`

**US-009:** As an Analyst, I want to load all my saved context at session start so I have continuity across conversations.
- Acceptance: `get_context` returns all insights, watchlist items, and segments

### Operations

**US-010:** As a Developer, I want a health check endpoint so I can verify the service is running.
- Acceptance: `GET /health` returns `{"status": "healthy"}`

**US-011:** As a Developer, I want to deploy with a single command so I can ship updates quickly.
- Acceptance: `make deploy` rsyncs, builds, restarts, and health-checks

**US-012:** As a Developer, I want pre-commit hooks to catch issues before they reach CI.
- Acceptance: `git commit` runs Black, pylint, and pytest automatically
