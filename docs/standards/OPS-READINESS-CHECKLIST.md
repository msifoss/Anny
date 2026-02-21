# Anny — Operational Readiness Checklist

**Last scored:** 2026-02-20
**Score:** 43/47 (91%)

---

## Scoring Key
- [x] = Passing (1 point)
- [ ] = Not passing (0 points)

---

## 1. Source Control & CI/CD (7 items)

- [x] 1.1 Code in version control (GitHub, main branch)
- [x] 1.2 Branch protection on main (PRs required)
- [x] 1.3 CI runs on every push/PR (GitHub Actions)
- [x] 1.4 CI includes format check (Black)
- [x] 1.5 CI includes linting (pylint 10/10)
- [x] 1.6 CI includes automated tests (unit + integration)
- [x] 1.7 CI includes deployment step (GitHub Actions: deploy job on push to main, after tests pass)

**Section: 7/7**

---

## 2. Testing (7 items)

- [x] 2.1 Unit tests exist (240 unit tests)
- [x] 2.2 Integration tests exist (11 integration tests)
- [x] 2.3 E2e tests exist (19 e2e tests, gated behind ANNY_E2E=1)
- [x] 2.4 Test coverage >= 80% (85%)
- [ ] 2.5 Pre-commit hooks run tests (removed — tests run via `make test` + CI)
- [ ] 2.6 Load/performance testing exists
- [x] 2.7 Smoke test runs automatically post-deploy (`scripts/smoke_test.sh` called from `deploy.sh`)

**Section: 5/7**

---

## 3. Security (8 items)

- [x] 3.1 Secrets excluded from version control (.gitignore patterns)
- [x] 3.2 HTTPS enforced in production (nginx TLS 1.2+, HSTS)
- [x] 3.3 Security headers configured (X-Frame-Options, X-Content-Type-Options, etc.)
- [x] 3.4 Firewall configured (UFW: 22/80/443 only)
- [x] 3.5 SSH hardened (fail2ban, key-only auth)
- [x] 3.6 Non-root container user (UID 1000)
- [x] 3.7 Dependency vulnerability scanning (pip-audit in CI)
- [x] 3.8 Security review conducted within last 30 days (2026-02-20, all findings resolved)

**Section: 8/8**

---

## 4. Authentication & Authorization (5 items)

- [x] 4.1 Service account auth for Google APIs (readonly scopes)
- [x] 4.2 API key auth for REST endpoints (X-API-Key header, ANNY_API_KEY env var, timing-safe comparison)
- [x] 4.3 Rate limiting configured (60 req/min per IP on /api/* and /mcp, in-memory)
- [x] 4.4 Localhost-only port binding in docker-compose
- [x] 4.5 CORS policy configured (CORSMiddleware, restrictive defaults, no open origins)

**Section: 5/5**

---

## 5. Monitoring & Observability (6 items)

- [x] 5.1 Structured logging (JSON via python-json-logger, request-ID tracking via contextvars)
- [x] 5.2 Log aggregation (in-memory ring buffer, `GET /api/logs` admin endpoint with level filtering)
- [x] 5.3 Health check endpoint (`GET /health` with dependency validation)
- [x] 5.4 Docker health check (HEALTHCHECK in Dockerfile)
- [x] 5.5 Uptime monitoring / alerting (`scripts/uptime_monitor.sh`, cron every 5 min, webhook alerts)
- [x] 5.6 Error tracking (Sentry via `sentry-sdk[fastapi]`, opt-in via SENTRY_DSN)

**Section: 6/6**

---

## 6. Deployment & Infrastructure (7 items)

- [x] 6.1 Docker containerization (multi-stage build)
- [x] 6.2 Docker Compose for orchestration
- [x] 6.3 Deploy script with health check validation (`scripts/deploy.sh`)
- [x] 6.4 SSL/TLS certificates (Let's Encrypt via certbot)
- [x] 6.5 Reverse proxy (nginx with WebSocket support)
- [x] 6.6 Automated rollback on failed deploy (`deploy.sh` tags current image, restores on health check failure)
- [ ] 6.7 Blue-green or canary deployment capability

**Section: 6/7**

---

## 7. Documentation (4 items)

- [x] 7.1 README with setup instructions
- [x] 7.2 CLAUDE.md (AI operating manual) current
- [x] 7.3 API documentation (REST endpoints + MCP tools documented)
- [x] 7.4 Runbook for incident response (`docs/manuals/INCIDENT-RESPONSE.md`)

**Section: 4/4**

---

## 8. Disaster Recovery (3 items)

- [x] 8.1 Backup strategy documented and tested (`docs/manuals/DR-PLAN.md`, `scripts/backup.sh`, daily cron)
- [x] 8.2 Recovery time objective (RTO) defined (30 minutes)
- [x] 8.3 Recovery point objective (RPO) defined (24 hours)

**Section: 3/3**

---

## Summary

| Category | Score | Pct |
|----------|-------|-----|
| Source Control & CI/CD | 7/7 | 100% |
| Testing | 5/7 | 71% |
| Security | 8/8 | 100% |
| Auth & Authorization | 5/5 | 100% |
| Monitoring & Observability | 6/6 | 100% |
| Deployment & Infrastructure | 6/7 | 86% |
| Documentation | 4/4 | 100% |
| Disaster Recovery | 3/3 | 100% |
| **Total** | **43/47** | **91%** |

---

## Changes from Last Score (42/47 → 43/47)

| Item | Change | Notes |
|------|--------|-------|
| 1.7 CD pipeline | [ ] → [x] | GitHub Actions deploy job on push to main, after tests pass |

Net change: +1

---

## Changes from Previous Score (37/47 → 42/47)

| Item | Change | Notes |
|------|--------|-------|
| 6.6 Automated rollback | [ ] → [x] | Bolt 9 — deploy.sh tags current image, restores on health check failure |
| 7.4 Incident response runbook | [ ] → [x] | Bolt 9 — `docs/manuals/INCIDENT-RESPONSE.md` |
| 8.1 Backup strategy | [ ] → [x] | Bolt 9 — DR plan + `scripts/backup.sh` (daily cron, 7-day retention) |
| 8.2 RTO defined | [ ] → [x] | Bolt 9 — 30 minutes (full VPS rebuild from scripts) |
| 8.3 RPO defined | [ ] → [x] | Bolt 9 — 24 hours (daily memory.json backup) |

Net change: +5

---

## Remaining Items (4 of 47)

| Item | Size | Notes |
|------|------|-------|
| 2.5 Pre-commit tests | S | Deliberately removed in Bolt 5 to speed commits; tests run via CI |
| 2.6 Load testing | M | Needs k6/locust setup |
| 6.7 Blue-green deploy | L | Overkill for single-container app |
