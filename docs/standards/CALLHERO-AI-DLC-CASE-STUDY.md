# Anny — AI-DLC Framework Alignment

**Last updated:** 2026-02-17

---

## Overview

This document maps Anny's development practices against the AI Development Lifecycle (AI-DLC) framework and tracks how the 10 identified shortcomings have been addressed.

## Shortcoming Resolution Status

| # | Shortcoming | Document | Status |
|---|------------|----------|--------|
| 1 | No formal Inception docs | `docs/REQUIREMENTS.md` | Addressed |
| 2 | No traceability matrix | `docs/TRACEABILITY-MATRIX.md` | Addressed |
| 3 | No Mob Elaboration | Five Questions in `docs/standards/SOLO-AI-WORKFLOW-GUIDE.md` | Addressed (adapted for solo+AI) |
| 4 | No CI/CD for deployment | `docs/standards/CICD-DEPLOYMENT-PROPOSAL.md` | Documented (CI exists, CD proposed) |
| 5 | No multi-dev patterns | `docs/standards/MULTI-DEVELOPER-GUIDE.md` | Addressed (guide ready for scaling) |
| 6 | Infrastructure undocumented | `docs/standards/INFRASTRUCTURE-PLAYBOOK.md` | Addressed |
| 7 | Cost management absent | `docs/standards/COST-MANAGEMENT-GUIDE.md` | Addressed |
| 8 | Security underspecified | `docs/standards/SECURITY-REVIEW-PROTOCOL.md` | Addressed |
| 9 | Ops readiness one-liner | `docs/standards/OPS-READINESS-CHECKLIST.md` | Addressed (scored 28/47) |
| 10 | Solo+AI not addressed | `docs/standards/SOLO-AI-WORKFLOW-GUIDE.md` | Addressed |

**Result: 10/10 shortcomings addressed**

## AI-DLC Phase Mapping

| AI-DLC Phase | Anny Equivalent | Evidence |
|-------------|----------------|---------|
| Inception | Requirements + User stories | `docs/REQUIREMENTS.md` |
| Elaboration | Plan mode + Five Questions | Bolt planning in `CURRENT-SPRINT.md` |
| Construction | Bolt execution (1-week sprints) | `docs/pm/SPRINT-LOG.md` |
| Transition | Deploy scripts + e2e tests | `scripts/deploy.sh`, `tests/e2e/` |
| Operations | OPS checklist + monitoring | `docs/standards/OPS-READINESS-CHECKLIST.md` |

## Key Adaptations for Solo+AI

The traditional AI-DLC framework assumes a team. Anny adapts:

- **Mob Elaboration → Five Questions:** Solo developer answers 5 structured questions before each session instead of mob programming
- **Code Review → Pre-commit hooks + AI review:** Automated format/lint/test gates replace human code review
- **Sprint Ceremonies → Bolt lifecycle:** `/pm` command replaces standup/retro meetings
- **Knowledge Management → CLAUDE.md + Memory Layer:** AI context is managed through structured documentation and MCP memory tools
