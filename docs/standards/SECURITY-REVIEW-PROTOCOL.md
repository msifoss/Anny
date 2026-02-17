# Security Review Protocol

**Project:** Anny
**Last updated:** 2026-02-17

---

## Review Cadence

| Trigger | Review Type |
|---------|------------|
| Every 30 days | Scheduled review |
| Before production deployment | Pre-deploy review |
| After major feature addition | Feature review |
| After dependency update | Supply chain review |

## Review Scope

Each review covers:

1. **OWASP Top 10** — Injection, auth failures, sensitive data exposure, etc.
2. **Cloud/Infrastructure** — Firewall rules, TLS config, container security
3. **Supply Chain** — `pip-audit` scan, dependency freshness
4. **Access Control** — API authentication, authorization boundaries
5. **Secrets Management** — Key rotation, file permissions, env var handling

## Review Process

1. Run automated scans: `make audit` (pip-audit)
2. Review all code changes since last audit
3. Check infrastructure configuration (nginx, Docker, UFW)
4. Document findings with severity (Critical/High/Medium/Low)
5. Write findings to `docs/security/security-audit-YYYY-MM-DD.md`
6. Update `SECURITY.md` audit status table
7. Create backlog items for any High+ findings

## Severity Definitions

| Level | Definition | SLA |
|-------|-----------|-----|
| Critical | Active exploitation possible, data breach risk | Fix immediately |
| High | Significant security gap, exploitable with effort | Fix within 1 Bolt |
| Medium | Defense-in-depth gap, low exploitability | Fix within 2 Bolts |
| Low | Best practice improvement, minimal risk | Fix when convenient |

## Review History

| Date | Findings | Notes |
|------|----------|-------|
| 2026-02-17 | 1H, 4M, 5L | Initial audit. H-001: REST API auth needed. |

## Next Review

**Scheduled:** 2026-03-17 (30 days from initial audit)
