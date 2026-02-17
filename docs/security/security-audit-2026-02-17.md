# Anny — Security Audit

**Date:** 2026-02-17
**Auditor:** Claude Code (AI-assisted)
**Scope:** Full application stack — source code, dependencies, infrastructure, deployment

---

## Executive Summary

Anny has a **strong security posture for a read-only analytics tool**. The readonly service account scopes, non-root Docker user, TLS enforcement, and firewall hardening are all correctly implemented. The primary gaps are the lack of API authentication for REST endpoints (anyone with network access can query analytics data) and missing rate limiting.

**Overall Risk Level:** MEDIUM (due to unauthenticated REST API on public internet)

---

## Findings

### CRITICAL: None

### HIGH

#### H-001: REST API has no authentication
**Location:** `src/anny/main.py`, all route files
**Risk:** Anyone who discovers `anny.membies.com` can query GA4, Search Console, and GTM data without credentials. While the data is read-only, analytics data can reveal business-sensitive information (traffic volumes, search queries, content strategy).
**Recommendation:** Implement API key authentication. Add a middleware or dependency that validates an `X-API-Key` header against a configured secret.
**Status:** Open (backlog item #14)

### MEDIUM

#### M-001: No rate limiting on any endpoint
**Location:** `src/anny/main.py`
**Risk:** An attacker could exhaust Google API quotas by making rapid requests, causing denial of service for legitimate users.
**Recommendation:** Add rate limiting middleware (e.g., `slowapi` or custom `X-RateLimit` headers). Consider per-IP and per-endpoint limits.
**Status:** Open (backlog item #12)

#### M-002: No CORS policy configured
**Location:** `src/anny/main.py`
**Risk:** Without explicit CORS configuration, the API could be called from any origin. While FastAPI defaults to no CORS (which blocks browser requests), an explicit policy is better practice.
**Recommendation:** Add `CORSMiddleware` with explicit `allow_origins`.
**Status:** Open

#### M-003: Memory store has no access control
**Location:** `src/anny/clients/memory.py`
**Risk:** Any MCP client can read/write/delete all memory entries. There's no concept of ownership or permissions for insights, watchlist items, or segments.
**Mitigation:** Low severity for single-user deployment. Would need addressing for multi-user scenarios.
**Status:** Accepted risk for current deployment model

#### M-004: Dependency vulnerability — diskcache CVE-2025-69872
**Location:** `requirements.txt` (transitive dependency)
**Risk:** `diskcache 5.6.3` has a known CVE. Severity and exploitability depend on CVE details.
**Recommendation:** Investigate CVE details. Update if a fix version is available, or pin to exclude if it's a transitive dependency not directly used.
**Status:** Open

### LOW

#### L-001: Health check exposes no dependency status
**Location:** `src/anny/main.py:22-24`
**Risk:** The `/health` endpoint returns `{"status": "healthy"}` without checking Google API connectivity. A misconfigured or expired service account would still report healthy.
**Recommendation:** Add dependency health checks (Google API reachability, credential validity).
**Status:** Open (backlog item #17)

#### L-002: Error messages may leak internal details
**Location:** `src/anny/core/auth.py:21`, `src/anny/api/error_handlers.py`
**Risk:** `AuthError` and `APIError` messages include file paths and exception details that could help an attacker understand the system.
**Mitigation:** The error handler returns `exc.message` directly. Consider sanitizing error messages in production.
**Status:** Accepted risk (low severity for internal tool)

#### L-003: No request/response logging
**Location:** Application-wide
**Risk:** No structured logging means security incidents (unusual query patterns, brute-force attempts) can't be detected or investigated.
**Recommendation:** Add structured JSON logging with request method, path, status code, and client IP.
**Status:** Open (backlog item #13)

#### L-004: Docker image uses `python:3.12-slim` base
**Location:** `Dockerfile`
**Risk:** The slim base image may contain known vulnerabilities in OS packages. No image scanning is configured.
**Recommendation:** Consider adding `trivy` or `grype` image scanning to CI pipeline.
**Status:** Informational

#### L-005: Memory store file permissions not explicitly set
**Location:** `src/anny/clients/memory.py`
**Risk:** The `~/.anny/memory.json` file is created with default umask permissions. On some systems this could be world-readable.
**Recommendation:** Set explicit `0o600` permissions on file creation.
**Status:** Open

---

## Supply Chain Analysis

### Direct Dependencies (8)

| Package | Version | Risk | Notes |
|---------|---------|------|-------|
| fastapi | >=0.115.0 | Low | Well-maintained, security-conscious |
| uvicorn | >=0.34.0 | Low | Standard ASGI server |
| python-dotenv | >=1.0.0 | Low | Minimal attack surface |
| pydantic-settings | >=2.0.0 | Low | Config loading only |
| google-auth | >=2.0.0 | Low | Google-maintained |
| google-analytics-data | >=0.18.0 | Low | Google-maintained |
| google-api-python-client | >=2.100.0 | Low | Google-maintained |
| fastmcp | >=2.0.0,<3 | Medium | Newer library, smaller community |

### Dev Dependencies (7)

| Package | Version | Risk | Notes |
|---------|---------|------|-------|
| pytest | >=8.0.0 | Low | Not in production |
| pytest-cov | >=6.0.0 | Low | Not in production |
| httpx | >=0.28.0 | Low | Test client only |
| black | >=25.1.0 | Low | Formatter only |
| pylint | >=3.3.0 | Low | Linter only |
| pip-audit | >=2.8.0 | Low | Auditor only |
| pre-commit | >=4.0.0 | Low | Git hooks only |

### pip-audit Results

```
Found 1 known vulnerability in 1 package
Name      Version ID             Fix Versions
--------- ------- -------------- ------------
diskcache 5.6.3   CVE-2025-69872
```

---

## Infrastructure Security Review

### VPS (Vultr)

| Control | Status | Notes |
|---------|--------|-------|
| UFW firewall | PASS | Ports 22, 80, 443 only |
| fail2ban | PASS | SSH brute-force protection |
| SSH key auth | PASS | Password auth disabled |
| Non-root deploy user | PASS | `deploy` user with sudo |
| TLS certificates | PASS | Let's Encrypt, auto-renewal via certbot |
| HSTS header | PASS | `max-age=63072000; includeSubDomains` |

### Docker

| Control | Status | Notes |
|---------|--------|-------|
| Non-root user | PASS | `anny` UID 1000 |
| Multi-stage build | PASS | Builder + runtime separation |
| Localhost port binding | PASS | `127.0.0.1:8000` |
| Log rotation | PASS | `max-size: 10m, max-file: 3` |
| Health check | PASS | `curl -f http://localhost:8000/health` |
| Read-only secrets mount | PASS | `:ro` flag on service account |
| Restart policy | PASS | `unless-stopped` |

---

## Recommendations Summary

| Priority | Finding | Action | Size |
|----------|---------|--------|------|
| HIGH | H-001: No API auth | Add API key middleware | M |
| MEDIUM | M-001: No rate limiting | Add slowapi or custom limiter | S |
| MEDIUM | M-002: No CORS | Add CORSMiddleware | S |
| MEDIUM | M-004: CVE in diskcache | Investigate and update/pin | S |
| LOW | L-001: Shallow health check | Add dependency checks | S |
| LOW | L-003: No structured logging | Add JSON logging | S |
| LOW | L-005: Memory file permissions | Set 0o600 on creation | S |

---

## Next Review

Schedule next security review for **2026-03-17** (30 days) or after the next feature addition, whichever comes first.
