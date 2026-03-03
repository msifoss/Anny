# Cross-Skill Recommendation Matrix

When to use each skill, what triggers it, and which skills to chain together.

---

## Skill Catalog

| Skill | Purpose | Trigger |
|-------|---------|---------|
| `/init-project` | Full project scaffold (callhero standard) | New project setup |
| `/pm` | Sprint management (status, plan, close, backlog, update, metrics) | Sprint lifecycle |
| `/motherhen` | Health & compliance monitor (7 checks, drift detection) | Routine hygiene sweep |
| `/dlc-audit` | Deep AI-DLC process assessment (9 dimensions, 0-10 scoring) | Phase transitions, milestone reviews |
| `/five-persona-review` | Multi-perspective code review (5 expert personas) | Pre-release, major features |
| `/security-audit` | Structured security audit (OWASP + cloud + supply chain) | Pre-deploy, 30-day cadence, post-feature |
| `/bolt-review` | End-of-sprint comprehensive review | Bolt close |
| `/changelog` | Keep-a-Changelog format updates | Post-release, post-feature |
| `/docs` | Documentation generation (README, CHANGELOG, SECURITY, manuals) | New project, major changes |
| `/readme` | README generation/update | After feature changes |
| `/captainslog` | Session log for AI context continuity | End of session |
| `/budget` | Infrastructure cost tracking and optimization | Monthly, after infra changes |
| `/cost-estimate` | Development effort estimation with AI-pair benchmarks | Pre-bolt planning |
| `/ticky` | Azure DevOps work item management | Ticket creation, sync |

---

## Chaining Guide

### Project Lifecycle

```
New Project:    /init-project → /pm plan → /cost-estimate → build
Sprint Start:   /pm plan → /cost-estimate
During Sprint:  build → /captainslog (end of session)
Sprint Close:   /bolt-review → /pm close → /changelog → /captainslog
Release:        /changelog → /five-persona-review → /security-audit → /docs → tag
```

### Routine Cadence

| Frequency | Skills |
|-----------|--------|
| Every session | `/captainslog` at end |
| Weekly | `/motherhen` (quick hygiene check) |
| Per bolt | `/pm` (open, track, close), `/bolt-review` at close |
| Per release | `/changelog`, `/five-persona-review`, `/security-audit` |
| Monthly | `/budget`, `/motherhen full` |
| Per phase transition | `/dlc-audit` (deep process assessment) |

### When Motherhen Flags Issues

| Motherhen Finding | Recommended Skill |
|-------------------|-------------------|
| AI-DLC Foundation WARN/FAIL | `/dlc-audit` — deep process assessment, bootstrap missing docs |
| AI-DLC Foundation FAIL (< 4 docs) | `/dlc-audit init` — create skeleton templates |
| Security Review FAIL (never reviewed) | `/security-audit` or `/five-persona-review` |
| Security Review WARN (stale) | `/security-audit` — refresh the audit |
| Sprint/PM stale or missing | `/pm status` — review current sprint state |
| Multiple FAIL items | `/pm plan` — open a bolt to address systematically |
| Documentation Drift FAIL | `/docs` — regenerate docs from current state |
| Release Hygiene FAIL | `/changelog` — update changelog, then tag |
| Context Freshness FAIL | Update CLAUDE.md manually (no skill needed) |
| Test Health FAIL | Fix tests directly (no skill needed) |

### When DLC-Audit Flags Issues

| DLC-Audit Finding | Recommended Skill |
|-------------------|-------------------|
| Low requirements score | Draft requirements manually or with `/init-project` patterns |
| Low testing score | Write tests directly, run `/motherhen focus:tests` to verify |
| Low security score | `/security-audit` — full OWASP + supply chain audit |
| Low PM score | `/pm` — establish sprint framework |
| Low documentation score | `/docs` — generate audience-specific guides |
| Low ops score | Review OPS-READINESS-CHECKLIST.md, address gaps in next bolt |

### Pre-Release Checklist

```
1. /motherhen full          — verify no FAIL items
2. /five-persona-review     — multi-perspective code review
3. /security-audit          — security posture check
4. /changelog               — ensure [Unreleased] is accurate
5. /bolt-review             — if closing a bolt simultaneously
6. Tag release, bump version
7. /docs                    — update README, manuals if needed
8. /captainslog             — record the session
```

### Anti-Patterns

| Don't | Do Instead |
|-------|-----------|
| Run `/dlc-audit` weekly | Use `/motherhen` weekly; `/dlc-audit` at phase transitions |
| Skip `/captainslog` | Always log at session end — future sessions depend on context |
| Run `/security-audit` after every commit | Run per release or every 30 days |
| Use `/five-persona-review` on trivial changes | Reserve for major features or pre-release |
| Run `/motherhen` and manually fix everything | Let motherhen offer to fix, or open a bolt |

---

## Skill Dependencies

```
/init-project ──→ /pm plan ──→ build ──→ /bolt-review ──→ /pm close
                                │                            │
                                ▼                            ▼
                          /captainslog               /changelog
                                                         │
                                                         ▼
                                                  /five-persona-review
                                                         │
                                                         ▼
                                                  /security-audit
                                                         │
                                                         ▼
                                                    tag release
                                                         │
                                                         ▼
                                                  /motherhen full
```

Standalone (no dependencies): `/budget`, `/cost-estimate`, `/ticky`, `/readme`

Monitoring loop: `/motherhen` → fix findings → `/motherhen` (verify fixes)

Deep audit loop: `/dlc-audit` → address gaps → `/dlc-audit` (re-score at next phase)
