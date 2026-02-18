# Bolt 5 — Production Hardening & Code Quality (2026-02-17)

**Goal:** Fix security vulnerabilities, add operational visibility, and harden error handling across the codebase

**Status:** IN PROGRESS

**Last updated:** 2026-02-17

---

## Items

| Item | Size | Status |
|------|------|--------|
| Fix timing attack in verify_api_key (hmac.compare_digest) | S | executable |
| Add file locking to MemoryStore | S | executable |
| Health check validates dependencies (creds, config, memory) | S | executable |
| Startup config validation (fail fast on missing config) | S | executable |
| Structured logging throughout app | M | executable |
| Fix bare except Exception in clients + auth | S | executable |
| Scrub credentials from error messages | S | executable |
| Add input bounds to MCP tools (match REST validation) | S | executable |
| Validate CSV fields in service layer | S | executable |
| Validate custom date ranges in date_utils | S | executable |
| Rate limiting middleware | M | executable |
| Move pytest out of pre-commit (keep format + lint only) | S | executable |

## Metrics

| Metric | Value |
|--------|-------|
| Commits | 0 |
| Tests | 154 collected / 135 unit+int passing / 19 e2e |
| Coverage | 82% |
| Deploys | 1 (anny.membies.com live) |
| MCP Tools | 21 |

## Blockers

| Blocker | Days Open | Notes |
|---------|-----------|-------|
| (none) | | |
