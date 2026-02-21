# Security Policy

## Reporting Vulnerabilities

If you discover a security vulnerability, report it privately:

- **Email:** (to be configured)
- **Scope:** Authentication bypass, data exposure, injection, privilege escalation

Do not test against production systems without authorization.

## Security Audit Status

| Round | Date | Findings | Status |
|-------|------|----------|--------|
| 4 | 2026-02-20 | 0 High, 1 Medium, 2 Low | 1 new (version drift), 2 accepted (known) |
| 3 | 2026-02-20 | 1 High, 3 Medium, 5 Low | All resolved (Bolt 8 review) |
| 2 | 2026-02-20 | 1 High, 6 Medium, 4 Low | All resolved (Bolt 6 + Bolt 7) |
| 1 | 2026-02-17 | 1 High, 4 Medium, 5 Low | All resolved (Bolt 5 + Bolt 6) |

See `docs/security/20260220-180000-security-audit.txt` for latest details.

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
- **At rest:** Service account key file on VPS filesystem (chmod 600, owner-only)
- **In transit:** HTTPS enforced via nginx (TLS 1.2+, HSTS)
- **Secrets:** Environment variables via `.env` — never commit secrets

### Input Validation
- Pydantic models for all request/response schemas
- FastAPI automatic request validation
- GTM account IDs and container paths regex-enforced
- CSV fields validated in service layer (reject empty metrics/dimensions)
- Date ranges validated (ISO format, start <= end)
- MCP tool input bounds clamped (MAX_LIMIT=100, MAX_ROW_LIMIT=1000)
- CSV export injection protection (formula-triggering characters prefixed with tab)
- Export route limit clamping (same bounds as MCP tools)

### Network Security
- UFW firewall: ports 22, 80, 443 only
- fail2ban for SSH brute-force protection
- Docker ports bound to localhost only (127.0.0.1:8000)
- nginx reverse proxy with security headers
- CORS middleware with restrictive defaults (no open origins)
- Rate limiting: 60 req/min per IP on `/api/*` and `/mcp` paths

### Container Security
- Non-root user (anny, UID 1000)
- Multi-stage Docker build
- Read-only secrets mount
- Log rotation configured
- Memory store file created with 0600 permissions (owner-only)

### Monitoring
- Docker health check (30s interval)
- nginx access/error logs
- Structured JSON logging with request-ID tracking
- In-memory ring buffer with admin `GET /api/logs` endpoint
- Sentry error tracking (opt-in via SENTRY_DSN)
- Uptime monitor script with webhook alerting (cron every 5 min)

## Dependency Management

```bash
# Run dependency vulnerability scan
pip-audit
```

All production dependencies pinned to exact versions in `requirements.txt`.

Last scan: 2026-02-20 — 1 vulnerability found (diskcache CVE-2025-69872, transitive via fastmcp; not used directly)

## Known Limitations
- No load/performance testing
- Gitleaks secret scanning only in pre-commit (not in CI)
