# Disaster Recovery Plan

**Project:** Anny
**Last updated:** 2026-02-20

---

## 1. Backup Strategy

### What to Back Up

| Asset | Location | Backup Method | Frequency |
|-------|----------|---------------|-----------|
| `memory.json` | `/home/anny/.anny/memory.json` (Docker volume) | `scripts/backup.sh` → `/opt/anny/backups/` | Daily (cron, 02:00 UTC) |
| `.env` | `/opt/anny/.env` (VPS) | Stored on operator's local machine + encrypted cloud storage | On change |
| Service account key | `/opt/anny/secrets/service-account.json` (VPS) | Stored on operator's local machine + Google Cloud Console (re-downloadable) | On change |
| nginx config | `/etc/nginx/sites-available/anny` (VPS) | `deploy/nginx-https.conf` in git repo | On change |

### What Does NOT Need Backup

| Asset | Reason |
|-------|--------|
| Application code | In git (GitHub) — `git clone` to restore |
| Docker images | Rebuilt from source via `docker compose build` |
| Google Analytics data | Ephemeral, re-queryable from Google APIs |
| Query cache | In-memory, ephemeral by design (TTL 3600s) |
| Log ring buffer | In-memory, ephemeral — historical logs in Docker/nginx |

### Backup Script

`scripts/backup.sh` copies `memory.json` from the Docker volume to `/opt/anny/backups/` with a timestamp. Retains 7 days of backups.

```bash
# Manual run
/opt/anny/scripts/backup.sh

# Cron setup (daily at 02:00 UTC)
# Add to deploy user's crontab:
0 2 * * * /opt/anny/scripts/backup.sh >> /var/log/anny-backup.log 2>&1
```

### Backup Verification

Periodically verify backups are running:

```bash
# Check backup directory
ls -la /opt/anny/backups/

# Verify latest backup is valid JSON
python3 -m json.tool /opt/anny/backups/$(ls -t /opt/anny/backups/ | head -1)
```

---

## 2. Recovery Time Objective (RTO)

**Target: 30 minutes**

### Rationale

| Scenario | Estimated Time | Steps |
|----------|---------------|-------|
| Container crash | 2 min | `docker compose restart` |
| Failed deploy | 5 min | Automated rollback via `deploy.sh` |
| Redeploy from git | 5 min | `rsync` + `docker compose build` + health check |
| New VPS provisioning | 20–30 min | `server-provision.sh` → `server-setup.sh` → `deploy.sh` → `ssl-setup.sh` |

The application is stateless with respect to Google API data — all analytics data is re-queryable. The only user-created state is `memory.json` (insights, watchlist, segments), which is small and backed up daily.

### Recovery Steps (Full VPS Loss)

```bash
# 1. Provision new VPS (~5 min)
make provision

# 2. Set up server (Docker, nginx, UFW, fail2ban) (~5 min)
make setup

# 3. Deploy application (~3 min)
make deploy

# 4. Set up SSL (~2 min)
make ssl-setup

# 5. Restore memory.json from backup (~1 min)
scp /local/backups/memory-latest.json deploy@NEW_IP:/opt/anny/backups/
ssh deploy@NEW_IP "docker cp /opt/anny/backups/memory-latest.json anny-anny-1:/home/anny/.anny/memory.json"

# 6. Configure cron (uptime monitor + backup) (~2 min)
ssh deploy@NEW_IP
crontab -e
# */5 * * * * /opt/anny/scripts/uptime_monitor.sh >> /var/log/anny-uptime.log 2>&1
# 0 2 * * * /opt/anny/scripts/backup.sh >> /var/log/anny-backup.log 2>&1

# 7. Verify
curl https://anny.membies.com/health
```

---

## 3. Recovery Point Objective (RPO)

**Target: 24 hours**

### Rationale

- `memory.json` is backed up daily at 02:00 UTC
- Memory data (insights, watchlist, segments) changes infrequently — a few times per Bolt session
- Losing up to 1 day of memory data is acceptable — insights can be re-derived from Google APIs
- All analytics data (GA4, Search Console, GTM) is stateless and re-queryable with zero data loss

### Data Loss Scenarios

| Scenario | Data at Risk | Impact |
|----------|-------------|--------|
| VPS disk failure | Up to 24h of memory.json changes | Low — insights re-derivable |
| Accidental file deletion | Up to 24h of memory.json changes | Low — restore from backup |
| Docker volume corruption | Up to 24h of memory.json changes | Low — restore from backup |
| Google API credential revocation | No data loss | Re-issue key from Google Cloud Console |

---

## 4. Disaster Recovery Test Schedule

| Test | Frequency | Method |
|------|-----------|--------|
| Verify backup files exist | Weekly | `ls /opt/anny/backups/` |
| Validate backup JSON | Monthly | `python3 -m json.tool <latest-backup>` |
| Test restore from backup | Quarterly | Restore to local Docker, verify contents |
| Full VPS rebuild | Annually | Provision new VPS, deploy, restore, verify |
