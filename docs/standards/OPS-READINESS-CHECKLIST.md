# Anny — Operational Readiness Checklist

**Last scored:** 2026-02-17
**Score:** 28/47 (60%)

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

- [x] 2.1 Unit tests exist (116 unit tests)
- [x] 2.2 Integration tests exist (11 integration tests)
- [x] 2.3 E2e tests exist (19 e2e tests, gated behind ANNY_E2E=1)
- [x] 2.4 Test coverage >= 80% (~81%)
- [x] 2.5 Pre-commit hooks run tests (pytest on every commit)
- [ ] 2.6 Load/performance testing exists
- [ ] 2.7 Smoke test runs automatically post-deploy (manual: `make smoke`)

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
- [ ] 3.8 Security review conducted within last 30 days

**Section: 7/8**

---

## 4. Authentication & Authorization (5 items)

- [x] 4.1 Service account auth for Google APIs (readonly scopes)
- [ ] 4.2 API key or token auth for REST endpoints (not implemented)
- [ ] 4.3 Rate limiting configured (not implemented)
- [x] 4.4 Localhost-only port binding in docker-compose
- [ ] 4.5 CORS policy configured (not implemented)

**Section: 2/5**

---

## 5. Monitoring & Observability (6 items)

- [ ] 5.1 Structured logging (JSON format)
- [ ] 5.2 Log aggregation (centralized log collection)
- [x] 5.3 Health check endpoint (`GET /health`)
- [x] 5.4 Docker health check (HEALTHCHECK in Dockerfile)
- [ ] 5.5 Uptime monitoring / alerting
- [ ] 5.6 Error tracking (Sentry or equivalent)

**Section: 2/6**

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
| Security | 7/8 | 88% |
| Auth & Authorization | 2/5 | 40% |
| Monitoring & Observability | 2/6 | 33% |
| Deployment & Infrastructure | 5/7 | 71% |
| Documentation | 3/4 | 75% |
| Disaster Recovery | 0/3 | 0% |
| **Total** | **28/47** | **60%** |

---

## Priority Actions to Reach 90% (42/47)

Need 14 more items. Highest-impact actions:

1. **API key auth** (4.2) — M, in backlog
2. **Rate limiting** (4.3) — S, in backlog
3. **Security review** (3.8) — M, in this session
4. **Structured logging** (5.1) — S, in backlog
5. **Smoke test post-deploy** (2.7) — S, add to deploy.sh
6. **Uptime monitoring** (5.5) — S, free tier (UptimeRobot/Healthchecks.io)
7. **CORS policy** (4.5) — S, FastAPI middleware
8. **Incident runbook** (7.4) — S, new doc
9. **CD step in CI** (1.7) — M, GitHub Actions deploy job
10. **Rollback on failed deploy** (6.6) — M, deploy.sh enhancement
