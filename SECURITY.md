# Security Policy

## Reporting Vulnerabilities

If you discover a security vulnerability, report it privately:

- **Email:** (to be configured)
- **Scope:** Authentication bypass, data exposure, injection, privilege escalation

Do not test against production systems without authorization.

## Security Audit Status

| Round | Date | Findings | Status |
|-------|------|----------|--------|
| 2 | 2026-02-20 | 1 High, 6 Medium, 4 Low | H-001 new (deploy.sh chmod) |
| 1 | 2026-02-17 | 1 High, 4 Medium, 5 Low | H-001 resolved (API key auth added) |

See `docs/security/20260220-143000-security-audit.txt` for latest details.

## Security Controls

### Authentication
- Google APIs: Service account with readonly scopes (GA4, SC, GTM)
- REST API: API key auth via `X-API-Key` header (`ANNY_API_KEY` env var)
- MCP HTTP: Bearer token auth via `Authorization: Bearer <ANNY_API_KEY>` (FastMCP DebugTokenVerifier)
- Health endpoint (`/health`) excluded from auth for monitoring

### Authorization
- All Google API scopes are readonly — no write access to any service
- No role-based access control (single-user deployment)

### Encryption
- **At rest:** Service account key file on VPS filesystem (chmod 644 — should be 600, see H-001)
- **In transit:** HTTPS enforced via nginx (TLS 1.2+, HSTS)
- **Secrets:** Environment variables via `.env` — never commit secrets

### Input Validation
- Pydantic models for all request/response schemas
- FastAPI automatic request validation

### Network Security
- UFW firewall: ports 22, 80, 443 only
- fail2ban for SSH brute-force protection
- Docker ports bound to localhost only (127.0.0.1:8000)
- nginx reverse proxy with security headers

### Container Security
- Non-root user (anny, UID 1000)
- Multi-stage Docker build
- Read-only secrets mount
- Log rotation configured

### Monitoring
- Docker health check (30s interval)
- nginx access/error logs
- No centralized log aggregation or alerting (yet)

## Dependency Management

```bash
# Run dependency vulnerability scan
pip-audit
```

Last scan: 2026-02-20 — 1 vulnerability found (diskcache CVE-2025-69872, transitive)

## Known Limitations
- Service account key chmod 644 on VPS (H-001 — should be 600)
- MCP endpoint exempt from rate limiting (M-001)
- No CORS policy (M-002)
- Google API errors passed through to clients (M-003)
- Memory store file has default permissions (M-004)
- Dependencies not pinned to exact versions (M-005)
- No centralized logging or alerting (M-006)
