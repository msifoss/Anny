# Multi-Developer Guide

**Project:** Anny
**Last updated:** 2026-02-17
**Status:** Not yet applicable (solo developer)

---

## When This Applies

Anny is currently developed by a solo developer + AI pair. This guide documents the patterns to adopt when/if additional developers join.

## Branching Strategy

**Recommended:** GitHub Flow (simple, PR-based)

- `main` is always deployable
- Feature branches: `feature/<name>` or `fix/<name>`
- All changes via PR with required reviews
- Squash merge to main

## Code Review Standards

- Every PR must pass CI (format, lint, test, audit)
- Reviewer checklist:
  - Does it follow existing patterns? (client → service → MCP/REST)
  - Are tests included?
  - Is CLAUDE.md updated if architecture changed?
  - Are there security implications?

## Conventions

- Follow patterns in `CLAUDE.md` — it's the source of truth
- Service layer is shared — never duplicate Google API logic in REST or MCP
- Lazy singletons via `@functools.lru_cache` in `dependencies.py`
- All MCP tools return text via `format_table()`
- Black (100 char), pylint 10/10, pytest on every commit

## Onboarding Checklist

1. Clone repo, `make install`
2. Read `CLAUDE.md` (full architecture overview)
3. Read `docs/REQUIREMENTS.md` (what the system does)
4. Copy `.env.example` to `.env`, configure service account
5. `make test` — verify all tests pass
6. `make lint` — verify pylint 10/10
7. Read `docs/pm/CURRENT-SPRINT.md` — understand current work
