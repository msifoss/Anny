# AI-DLC Case Study: Anny

**Project:** Anny — Conversational Analytics Tool
**Duration:** 17 days (2026-02-13 to 2026-03-02)
**Developer:** Solo + AI pair (Claude)
**Stack:** Python 3.12, FastAPI, Google APIs, Docker, Vultr VPS

---

## Overview

Anny is a conversational analytics tool that gives LLMs and programmatic clients access to Google Analytics 4, Search Console, and Tag Manager. Built by a solo developer paired with Claude, the project reached 91% operational readiness in 17 days — demonstrating how AI-DLC practices accelerate project maturity without sacrificing quality or security.

---

## Timeline & Bolt Progression

| Bolt | Date | Focus | Key Deliverables |
|------|------|-------|-----------------|
| 1 | Feb 13-14 | Core Build | GA4, SC, GTM integration; 12 MCP tools; 88 tests |
| 2 | Feb 14-16 | Deploy & Test | Docker, Vultr VPS, e2e tests, smoke tests |
| 3 | Feb 16-17 | Pivot | Closed early; pivoted to memory layer |
| 4 | Feb 17 | Memory Layer | MemoryStore, 9 MCP tools, API key auth |
| 5 | Feb 17-18 | Hardening | 12 security items: timing attack, file locking, rate limiting |
| 6 | Feb 20 | Security Audit | 11 findings resolved (1H, 6M, 4L); MCP Bearer auth |
| 7 | Feb 20 | Observability | JSON logging, Sentry, request-ID tracking, admin logs |
| 8 | Feb 20 | Feature Expansion | Query cache, GA4 realtime, SC sitemaps, CSV/JSON export |
| 9 | Feb 20 | OPS Readiness | Incident runbook, DR plan, automated rollback, backup |

Post-bolt work: config centralization (v0.9.0), CD pipeline, five-persona code review, compliance fixes.

---

## Metrics Progression

| Metric | Bolt 1 | Bolt 5 | Bolt 9 | Current |
|--------|--------|--------|--------|---------|
| Tests | 88 | 164 | 270 | 275 |
| Coverage | 86% | 83% | 85% | 83% |
| Pylint | 10/10 | 10/10 | 10/10 | 10/10 |
| MCP Tools | 12 | 21 | 26 | 26 |
| REST Endpoints | 13 | 13 | 25 | 25 |
| OPS Readiness | — | — | 42/47 | 43/47 (91%) |
| Security Findings | — | 10 resolved | 21 resolved | 21 resolved |
| Deploys | 0 | 1 | 8 | 9 |

---

## AI-DLC Practices Applied

### 1. Structured Sprint Framework (Bolts)

One-week sprints with clear goal statements, T-shirt sizing, and mandatory retros. Each bolt archived in `SPRINT-LOG.md` with metrics and "went well / improve / action" format. Pivoting is accepted (Bolt 3 closed early when priorities shifted).

### 2. Five Questions Pre-Work Pattern

Before each session: goal, scope, out-of-scope, blockers, exit criteria. Replaces synchronous mob elaboration with structured solo+AI planning. Documented in `SOLO-AI-WORKFLOW-GUIDE.md`.

### 3. Continuous Quality Gates

Pre-commit hooks (Black, pylint, gitleaks) enforce standards on every commit. CI pipeline adds coverage floor (80%) and pylint gate (9.5). No commit bypasses formatting or linting.

### 4. Security Review Cadence

Three audit rounds resolved 21 findings (1 High, 10 Medium, 10 Low). Reviews triggered at 30-day intervals, pre-deploy, and post-feature. Five-persona code review added a multi-perspective lens. All findings tracked in `SECURITY.md` with severity and remediation status.

### 5. Operational Readiness Scoring

47-item checklist across 8 categories scored from day one. Score tracked through every bolt: initial → 28/47 → 43/47 (91%). Remaining gaps (load testing, pre-commit tests) honestly documented rather than inflated.

### 6. Traceability

Requirements matrix (13 FR, 8 NFR, 9 SEC) mapped to source files and tests in `TRACEABILITY-MATRIX.md`. Every feature traceable from requirement to implementation to test.

### 7. Documentation as Source of Truth

`CLAUDE.md` serves as the AI operating manual — architecture, conventions, current status. Updated at session boundaries. Complemented by `README.md`, `SECURITY.md`, `CHANGELOG.md`, and 8 standards documents.

---

## Solo+AI Adaptations

Traditional AI-DLC assumes a team. Solo+AI required these adaptations:

| Traditional Practice | Solo+AI Adaptation |
|---------------------|-------------------|
| Mob elaboration | Five Questions pattern (structured async) |
| Peer code review | Pre-commit hooks + five-persona AI review |
| Sprint ceremonies | `/pm` command automates standup/retro/metrics |
| Team onboarding | CLAUDE.md as single source of truth |
| Knowledge sharing | Memory service (9 MCP tools) persists context across sessions |

---

## Key Lessons

**Velocity without vigilance is speed toward a cliff.** Bolt 8 shipped four features in one session. Post-delivery security review caught CSV injection before production. The lesson: fast delivery demands immediate security review.

**Documentation drift accumulates silently.** Mother Hen compliance monitoring caught 4 drifting metrics (coverage percentages, test counts, stale dates) that manual review missed. Automated compliance checks are essential for solo developers who lack a second pair of eyes.

**Honest scoring beats inflated scoring.** The OPS checklist never marks items done until they truly are. Four items remain open (load testing, pre-commit tests). This honesty makes the score meaningful and trustworthy.

**Pivot early, not late.** Bolt 3 was closed and pivoted when the memory layer became higher priority. The cost of closing a bolt early is near zero; the cost of forcing misaligned work is high.

**Plan operations from day one.** Incident response runbook and DR plan were written on day 7, not after the first incident. Backup scripts and automated rollback existed before they were needed.

---

## AI-DLC Shortcomings Addressed

All 10 AI-DLC shortcomings identified in the framework have been addressed:

| # | Shortcoming | Document | Status |
|---|-------------|----------|--------|
| 1 | Inception docs | `docs/REQUIREMENTS.md` | Complete |
| 2 | Traceability matrix | `docs/TRACEABILITY-MATRIX.md` | Complete |
| 3 | Mob elaboration | `docs/standards/SOLO-AI-WORKFLOW-GUIDE.md` | Adapted |
| 4 | CI/CD for deployment | `.github/workflows/ci.yml` | Complete |
| 5 | Multi-dev patterns | `docs/standards/MULTI-DEVELOPER-GUIDE.md` | Ready |
| 6 | Infrastructure docs | `docs/standards/INFRASTRUCTURE-PLAYBOOK.md` | Complete |
| 7 | Cost management | `docs/standards/COST-MANAGEMENT-GUIDE.md` | Complete |
| 8 | Security specification | `docs/standards/SECURITY-REVIEW-PROTOCOL.md` | Complete |
| 9 | Ops readiness | `docs/standards/OPS-READINESS-CHECKLIST.md` | 91% |
| 10 | Solo+AI practices | `docs/standards/SOLO-AI-WORKFLOW-GUIDE.md` | Complete |

---

## Results

- **275 tests** (245 unit, 11 integration, 19 e2e), 83% coverage, pylint 10/10
- **26 MCP tools** and **25 REST endpoints** across 3 Google services
- **43/47 (91%) OPS readiness** with incident response, DR, and automated rollback
- **21 security findings** resolved across 3 audit rounds
- **9 production deploys** to anny.membies.com with zero downtime
- **14/14 AI-DLC foundational documents** present
- **$6/month** infrastructure cost (Vultr VPS)

The project demonstrates that AI-DLC practices — when adapted for solo+AI development — can produce production-ready software with enterprise-grade compliance in weeks rather than months.
