# CI/CD Deployment Proposal

**Project:** Anny
**Last updated:** 2026-02-17
**Status:** Proposal (not yet implemented)

---

## Current State

- CI: GitHub Actions runs format-check, lint, test, pip-audit on push/PR to main
- CD: Manual deployment via `make deploy` (rsync + docker compose on Vultr VPS)
- No automated deployment on merge to main

## Proposed Pipeline

```
Push to main
    │
    ├── CI (existing) ─────────────────────────────────┐
    │   ├── Black format check                         │
    │   ├── Pylint lint                                │
    │   ├── pytest (unit + integration)                │
    │   └── pip-audit                                  │
    │                                                  │
    │   All pass?                                      │
    │   ├── No → Stop, notify                          │
    │   └── Yes ↓                                      │
    │                                                  │
    ├── CD (new) ──────────────────────────────────────┤
    │   ├── Build Docker image                         │
    │   ├── SSH to VPS                                 │
    │   ├── Pull and restart container                 │
    │   ├── Health check (30s timeout)                 │
    │   ├── Pass → Done                                │
    │   └── Fail → Rollback to previous image          │
    └──────────────────────────────────────────────────┘
```

## Requirements

1. GitHub Actions secrets: SSH key, VPS IP, deploy user
2. Docker image tagging strategy (git SHA or semver)
3. Rollback mechanism (keep previous image, restore on health check failure)
4. Post-deploy smoke test

## Risks

- Single VPS = no zero-downtime deployment (brief outage during restart)
- SSH key in GitHub secrets = attack surface
- No staging environment for pre-prod validation

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| GitHub Actions CD | Simple, integrated | SSH key management |
| Docker Hub + Watchtower | Auto-pull on push | Less control over rollback |
| Manual deploy (current) | Full control | Human error, forgotten deploys |

## Decision

Defer until API auth (H-001) is implemented. No point automating deployment of an unauthenticated API.
