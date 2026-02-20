# Incident Response Runbook

**Project:** Anny
**Last updated:** 2026-02-20

---

## 1. Detection

Incidents are detected through:

| Channel | What It Catches | Response Time |
|---------|----------------|---------------|
| Uptime monitor (`scripts/uptime_monitor.sh`) | Service down, health check failures | 5 min (cron interval) |
| Sentry alerts (`SENTRY_DSN`) | Unhandled exceptions, error spikes | Near-realtime |
| Health check endpoint (`GET /health`) | Dependency failures (config, creds, memory) | On-demand |
| Admin logs (`GET /api/logs`) | Error patterns, request failures | On-demand |
| User reports | Functional issues not caught by monitoring | Variable |

---

## 2. Severity Levels

| Level | Definition | Examples | Target Response |
|-------|-----------|----------|-----------------|
| **P1 — Critical** | Service is down or completely unusable | Container crash, health check failing, TLS cert expired, nginx down | 30 min |
| **P2 — Degraded** | Service is up but partially broken | One API integration failing (GA4/SC/GTM), high error rate, slow responses | 4 hours |
| **P3 — Minor** | Cosmetic or low-impact issue | Incorrect formatting in MCP output, stale cache data, non-critical log noise | Next Bolt |

---

## 3. Response Steps

### P1 — Service Down

```
1. Verify the outage
   curl -sf https://anny.membies.com/health

2. SSH to server
   ssh deploy@anny.membies.com

3. Check container status
   cd /opt/anny && docker compose ps

4. Check container logs (last 200 lines)
   docker compose logs --tail 200

5. Check nginx status
   sudo systemctl status nginx
   sudo tail -50 /var/log/nginx/error.log

6. Restart container (if crashed)
   docker compose restart

7. If restart fails — rebuild
   docker compose build && docker compose up -d

8. If build fails — rollback to previous image
   # deploy.sh handles this automatically on failed deploys
   # For manual rollback:
   docker compose down
   docker tag anny:rollback anny-anny:latest
   docker compose up -d

9. Verify recovery
   curl -sf https://anny.membies.com/health
```

### P2 — Degraded Service

```
1. Check admin logs for error patterns
   curl -H "X-API-Key: $ANNY_API_KEY" https://anny.membies.com/api/logs?level=ERROR

2. Check Sentry for recent exceptions
   (Visit Sentry dashboard)

3. Identify which integration is failing
   curl -H "X-API-Key: $ANNY_API_KEY" https://anny.membies.com/api/ga4/realtime
   curl -H "X-API-Key: $ANNY_API_KEY" https://anny.membies.com/api/search-console/summary
   curl -H "X-API-Key: $ANNY_API_KEY" https://anny.membies.com/api/tag-manager/accounts

4. Check if it's a Google API issue
   - Service account key expired? → Regenerate in Google Cloud Console
   - API quota exceeded? → Check Google Cloud Console quotas
   - API outage? → Check Google Workspace Status Dashboard

5. If application bug — hotfix
   - Fix locally, run `make test`
   - Deploy: `make deploy`
```

### P3 — Minor Issue

```
1. Log the issue in captain's log
2. Add to backlog for next Bolt
3. No immediate action required
```

---

## 4. Escalation

Anny is a single-operator project. There is no on-call rotation.

| Trigger | Action |
|---------|--------|
| Uptime monitor detects DOWN | Webhook alert sent to `ALERT_WEBHOOK_URL` (configured in cron) |
| Sentry captures exception | Email notification to project owner |
| P1 not resolved in 30 min | Operator investigates VPS provider status (Vultr) |

---

## 5. Communication

| Audience | Channel | When |
|----------|---------|------|
| MCP clients (Claude) | Service returns error responses automatically | Immediate |
| REST API consumers | HTTP 502/503 status codes | Immediate |
| Project stakeholders | Direct notification (email/message) | After P1 confirmed |

---

## 6. Post-Incident

After every P1 or P2 incident:

1. **Captain's log entry** — Record what happened, timeline, and resolution
2. **Root cause analysis** — Identify why it happened (1-2 sentences is fine)
3. **OPS checklist review** — Would any new check have caught this earlier?
4. **Prevention** — Add monitoring, test, or documentation to prevent recurrence

---

## 7. Quick Reference Commands

```bash
# SSH to server
ssh deploy@anny.membies.com

# Container status
cd /opt/anny && docker compose ps

# Container logs (last 100 lines)
docker compose logs --tail 100

# Follow logs in realtime
docker compose logs -f

# Restart container
docker compose restart

# Rebuild and restart
docker compose build && docker compose up -d

# Check nginx
sudo systemctl status nginx
sudo nginx -t
sudo systemctl reload nginx

# Check disk space
df -h

# Check memory
free -m

# Check running processes
htop

# Manual health check
curl -sf https://anny.membies.com/health | python3 -m json.tool

# Check admin logs (from remote)
curl -H "X-API-Key: $ANNY_API_KEY" "https://anny.membies.com/api/logs?level=ERROR&limit=50"

# Run backup manually
/opt/anny/scripts/backup.sh

# Deploy (from local machine)
make deploy
```
