# Anny — Operational Readiness Checklist

**Last scored:** 2026-02-20
**Score:** 37/47 (79%)

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
- [ ] 1.7 CI includes deployment step (CD not implemented — manual deploy via `make deploy`)

**Section: 6/7**

---

## 2. Testing (7 items)

- [x] 2.1 Unit tests exist (219 unit tests)
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
- [ ] 6.6 Automated rollback on failed deploy
- [ ] 6.7 Blue-green or canary deployment capability

**Section: 5/7**

---

## 7. Documentation (4 items)

- [x] 7.1 README with setup instructions
- [x] 7.2 CLAUDE.md (AI operating manual) current
- [x] 7.3 API documentation (REST endpoints + MCP tools documented)
- [ ] 7.4 Runbook for incident response

**Section: 3/4**

---

## 8. Disaster Recovery (3 items)

- [ ] 8.1 Backup strategy documented and tested
- [ ] 8.2 Recovery time objective (RTO) defined
- [ ] 8.3 Recovery point objective (RPO) defined

**Section: 0/3**

---

## Summary

| Category | Score | Pct |
|----------|-------|-----|
| Source Control & CI/CD | 6/7 | 86% |
| Testing | 5/7 | 71% |
| Security | 8/8 | 100% |
| Auth & Authorization | 5/5 | 100% |
| Monitoring & Observability | 6/6 | 100% |
| Deployment & Infrastructure | 5/7 | 71% |
| Documentation | 3/4 | 75% |
| Disaster Recovery | 0/3 | 0% |
| **Total** | **37/47** | **79%** |

---

## Changes from Last Score (31/47 → 37/47)

| Item | Change | Notes |
|------|--------|-------|
| 2.1 Unit tests | updated | 134 → 171 unit tests |
| 2.4 Coverage | updated | 83% → 85% |
| 2.7 Smoke test post-deploy | [ ] → [x] | Bolt 7 — smoke_test.sh called from deploy.sh |
| 4.5 CORS policy | [ ] → [x] | Bolt 6 — CORSMiddleware with restrictive defaults |
| 5.1 Structured logging | updated | Text → JSON (python-json-logger + request-ID) |
| 5.2 Log aggregation | [ ] → [x] | Bolt 7 — ring buffer + GET /api/logs endpoint |
| 5.5 Uptime monitoring | [ ] → [x] | Bolt 7 — uptime_monitor.sh, cron */5, webhook alerts |
| 5.6 Error tracking | [ ] → [x] | Bolt 7 — Sentry via sentry-sdk[fastapi] |

Net change: +6

---

## Priority Actions to Reach 90% (42/47)

Need 5 more items. Highest-impact actions:

1. **Incident runbook** (7.4) — S, new doc
2. **Backup strategy** (8.1) — S, document strategy for memory.json + .env
3. **RTO/RPO** (8.2, 8.3) — S, define in ops docs
4. **CD step in CI** (1.7) — M, GitHub Actions deploy job
5. **Rollback on failed deploy** (6.6) — M, deploy.sh enhancement
6. **Pre-commit tests or equivalent** (2.5) — S, re-add if desired
7. **Load testing** (2.6) — M, basic k6/locust script
8. **Blue-green deploy** (6.7) — L, requires infra changes
