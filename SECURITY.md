# Security Policy

## Reporting Vulnerabilities

If you discover a security vulnerability, report it privately:

- **Email:** (to be configured)
- **Scope:** Authentication bypass, data exposure, injection, privilege escalation

Do not test against production systems without authorization.

## Security Audit Status

| Round | Date | Findings | Status |
|-------|------|----------|--------|
| — | — | — | No audits yet |

## Security Controls

### Authentication
- (To be implemented)

### Authorization
- (To be implemented)

### Encryption
- **At rest:** (To be configured)
- **In transit:** HTTPS enforced
- **Secrets:** Environment variables via `.env` — never commit secrets

### Input Validation
- Pydantic models for all request/response schemas
- FastAPI automatic request validation

### Monitoring
- (To be configured)

## Known Limitations
- (Document as they arise)

## Dependency Updates

```bash
# Run dependency vulnerability scan
pip-audit
```
