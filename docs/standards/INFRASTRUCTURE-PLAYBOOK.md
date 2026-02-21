# Anny — Infrastructure Playbook

**Last updated:** 2026-02-20

This document describes Anny's production infrastructure: how it's provisioned, configured, deployed, and maintained.

---

## Architecture Overview

```
Internet → DNS (anny.membies.com)
              │
              ▼
┌──────────────────────────────────────────────────┐
│  Vultr VPS (vc2-1c-1gb, Ubuntu 24.04, ewr)      │
│                                                  │
│  ┌──────────────────────────────────────┐       │
│  │  nginx (reverse proxy)               │       │
│  │  - Port 80 → 301 redirect to HTTPS   │       │
│  │  - Port 443 → proxy to :8000         │       │
│  │  - TLS 1.2/1.3 (Let's Encrypt)      │       │
│  │  - Security headers (HSTS, CSP, etc) │       │
│  └──────────────┬───────────────────────┘       │
│                 │                                │
│  ┌──────────────▼───────────────────────┐       │
│  │  Docker (anny-anny-1)                │       │
│  │  - Python 3.12 slim                  │       │
│  │  - FastAPI + uvicorn on :8000        │       │
│  │  - Non-root user (anny:1000)         │       │
│  │  - Health check every 30s            │       │
│  │  Volumes:                            │       │
│  │  - /secrets/service-account.json (RO)│       │
│  │  - /app/config.yaml (RO)            │       │
│  │  - anny-memory → /home/anny/.anny   │       │
│  └──────────────────────────────────────┘       │
│                                                  │
│  Security:                                       │
│  - UFW: 22 (rate-limited), 80, 443 only         │
│  - fail2ban: SSH brute-force protection          │
│  - deploy user (non-root, scoped sudo)           │
│  - Docker port bound to 127.0.0.1 only          │
└──────────────────────────────────────────────────┘
```

---

## Components

| Component | Version | Config |
|-----------|---------|--------|
| OS | Ubuntu 24.04 (Vultr) | `scripts/server-setup.sh` |
| Docker | Latest (official repo) | Installed via server-setup |
| nginx | System package | `deploy/nginx-https.conf` |
| certbot | System package | Let's Encrypt, auto-renewal timer |
| UFW | System package | 22 (rate-limited), 80, 443 only |
| fail2ban | System package | SSH: 5 retries, 1h ban, 10m window |
| Python | 3.12-slim | `Dockerfile` base image |
| uvicorn | >=0.34.0 | ASGI server |

---

## Deployment Flow

```
1. make provision  → Create Vultr VPS + DNS A record
2. make setup      → Bootstrap Docker, nginx, UFW, fail2ban
3. make deploy     → rsync + docker build + health check + rollback
4. make ssl        → Let's Encrypt certificate + HTTPS nginx config
5. Cron jobs       → backup.sh (daily 2AM), uptime_monitor.sh (5min)
```

All scripts read configuration from `config.yaml` via `scripts/config-get`, falling back to hardcoded defaults.

---

## 1. VPS Provisioning (`make provision`)

**Script:** `scripts/server-provision.sh`
**Prerequisites:** `VULTR_API_KEY` env var, SSH key registered on Vultr

### Process
1. Looks up SSH key by name via Vultr API
2. Creates VPS instance (plan, region, OS from config.yaml)
3. Polls until `active` + `running` (timeout: 5 min)
4. Creates DNS A record: `anny.membies.com` → instance IP (TTL: 300s)
5. Saves IP to `.server-ip` for subsequent scripts

### Configuration (config.yaml)
```yaml
infra:
  vultr_plan: "vc2-1c-1gb"
  vultr_region: "ewr"
  vultr_os_id: "2284"
  vultr_label: "anny"
  parent_domain: "membies.com"
  subdomain: "anny"
  ssh_key_name: "webengine-deploy"
```

---

## 2. Server Setup (`make setup`)

**Script:** `scripts/server-setup.sh`
**Prerequisites:** SSH access as root, `.server-ip` file

### Process
1. Waits for SSH connectivity (30 attempts, 5s apart)
2. Updates system packages
3. Installs: nginx, certbot, ufw, fail2ban, jq, Docker (official repo)
4. Creates `deploy` user (non-root, docker group)
5. Configures scoped sudo (nginx, certbot, config copy only)
6. Configures UFW: deny all, limit SSH, allow 80/443
7. Configures fail2ban: 5 retries, 1h ban, 10m window
8. Deploys HTTP nginx config (temporary, for certbot)
9. Creates `/opt/anny/` and `/opt/anny/secrets/` (mode 700)

### Scoped Sudo for deploy User
```
nginx -t
systemctl reload/restart nginx
certbot *
cp /tmp/anny-https.conf /etc/nginx/sites-enabled/anny.conf
```

---

## 3. Deployment (`make deploy`)

**Script:** `scripts/deploy.sh`
**Prerequisites:** `.env` file, service account key, SSH as `deploy`

### Process
1. **Preflight:** Verify `.env` and service account key exist
2. **Rsync** to `/opt/anny/`: Dockerfile, docker-compose.yml, requirements.txt, pyproject.toml, config.yaml, src/
3. **Upload secrets:** `.env` and service account key via SCP
4. **Tag rollback:** Current running image tagged as `anny:rollback`
5. **Build and start:** `docker compose build && docker compose up -d`
6. **Health check:** Poll `/health` every 5s for 60s
7. **On success:** Run smoke test (if available), exit 0
8. **On failure:** Restore rollback image, restart, exit 1

### Automatic Rollback
If health check fails and a previous image exists, the script automatically:
- Stops the failed container
- Retags the rollback image as latest
- Restarts with the previous version

---

## 4. SSL/TLS Setup (`make ssl`)

**Script:** `scripts/ssl-setup.sh`
**Prerequisites:** `CERTBOT_EMAIL` env var, HTTP config running, DNS resolving

### Process
1. Verifies DNS resolution matches server IP
2. Requests Let's Encrypt certificate (webroot method)
3. Deploys HTTPS nginx config
4. Tests and reloads nginx
5. Verifies `https://anny.membies.com/health` returns 200

### TLS Configuration
| Setting | Value |
|---------|-------|
| Protocols | TLSv1.2, TLSv1.3 only |
| Ciphers | ECDHE + AES-GCM / ChaCha20-Poly1305 |
| HSTS | max-age=63072000 (2 years), includeSubDomains |
| Session cache | 10 MB shared, 1-day timeout |
| Session tickets | Disabled |
| Renewal | Automatic via certbot systemd timer |

### Security Headers
| Header | Value |
|--------|-------|
| Strict-Transport-Security | max-age=63072000; includeSubDomains |
| X-Frame-Options | DENY |
| X-Content-Type-Options | nosniff |
| Referrer-Policy | strict-origin-when-cross-origin |
| Permissions-Policy | camera=(), microphone=(), geolocation=() |

---

## 5. Backup (`scripts/backup.sh`)

**Schedule:** Daily at 2 AM via cron
**Retention:** 7 days

### Process
1. Copies `memory.json` from container to `/opt/anny/backups/`
2. Filename: `memory-YYYYMMDD-HHMMSS.json`
3. Deletes backups older than 7 days

### Cron Entry
```
0 2 * * * /opt/anny/scripts/backup.sh >> /var/log/anny-backup.log 2>&1
```

### Configuration (config.yaml)
```yaml
backup:
  dir: "/opt/anny/backups"
  container_name: "anny-anny-1"
  data_path: "/home/anny/.anny/memory.json"
  retention_days: 7
```

---

## 6. Uptime Monitoring (`scripts/uptime_monitor.sh`)

**Schedule:** Every 5 minutes via cron
**Alerting:** Webhook (Slack/Discord) on state transitions only

### Process
1. Curls health endpoint with 10s timeout
2. Tracks UP/DOWN state in `/tmp/anny-uptime-state`
3. Sends webhook alert only on transitions (UP→DOWN, DOWN→UP)
4. Suppresses repeat alerts for continued downtime

### Cron Entry
```
*/5 * * * * /opt/anny/scripts/uptime_monitor.sh
```

Set `ALERT_WEBHOOK_URL` env var for Slack/Discord notifications.

---

## 7. Docker Configuration

### Dockerfile (Multi-Stage)

| Stage | Base | Purpose |
|-------|------|---------|
| builder | python:3.12-slim | pip install + editable install |
| runtime | python:3.12-slim | Copy packages + source, non-root user |

- **User:** `anny` (UID 1000, GID 1000)
- **Port:** 8000
- **Health check:** `curl -f http://localhost:8000/health` (30s interval, 5s timeout, 3 retries)
- **Entrypoint:** `uvicorn src.anny.main:app --host 0.0.0.0 --port 8000`

### docker-compose.yml

- **Port binding:** `127.0.0.1:8000:8000` (localhost only — nginx proxies)
- **Restart:** `unless-stopped`
- **Logging:** json-file, 10 MB max, 3 files (rotate at ~30 MB)
- **Volumes:**
  - `./secrets/service-account.json:/secrets/service-account.json:ro`
  - `./config.yaml:/app/config.yaml:ro`
  - `anny-memory:/home/anny/.anny` (named volume, persistent)

---

## 8. Secrets

| Secret | Location (VPS) | Location (Dev) |
|--------|---------------|----------------|
| Service account key | `/opt/anny/secrets/service-account.json` | Local path in `.env` |
| Environment config | `/opt/anny/.env` | `.env` in project root |
| SSH deploy key | `~deploy/.ssh/authorized_keys` | `~/.ssh/webengine_deploy` |
| API key | In `.env` (ANNY_API_KEY) | In `.env` |

---

## 9. VPS Directory Layout

```
/opt/anny/                          # App root (owned by deploy:deploy)
├── src/                            # Source code (rsync'd)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pyproject.toml
├── config.yaml
├── .env                            # Secrets (SCP'd by deploy.sh)
├── scripts/                        # Operational scripts
├── secrets/
│   └── service-account.json        # Google SA key (RO mount)
└── backups/
    └── memory-YYYYMMDD-HHMMSS.json # Daily backups (7-day retention)

/etc/nginx/sites-enabled/
└── anny.conf                       # HTTPS config

/etc/letsencrypt/live/anny.membies.com/
├── fullchain.pem                   # TLS certificate
└── privkey.pem                     # Private key

/var/log/
├── nginx/anny.access.log
├── nginx/anny.error.log
└── anny-backup.log                 # Backup cron log
```

---

## 10. Configuration Precedence

Settings are resolved in this order (first wins):

1. **Environment variable** (e.g., `ANNY_API_KEY`)
2. **`.env` file** (loaded by pydantic-settings)
3. **`config.yaml`** (flattened: `deploy.domain` → `deploy_domain`)
4. **Code default** (in `Settings` class)

Secrets (API keys, DSNs) should only be in `.env`, never in `config.yaml`.

---

## 11. Security Summary

| Layer | Control |
|-------|---------|
| Network | UFW: 22 (rate-limited), 80, 443 only |
| SSH | Key-only auth, fail2ban (5 retries, 1h ban) |
| User | Non-root `deploy` user with scoped sudo |
| Container | Non-root `anny:1000`, localhost-only port |
| TLS | TLSv1.2+, modern ciphers, HSTS |
| Headers | X-Frame-Options, X-Content-Type, Referrer-Policy |
| Auth | API key (timing-safe), rate limiting (60 req/min) |
| Secrets | `.gitignore` patterns, volume mounts (RO) |
| Deploy | Automated rollback on health check failure |
| Monitoring | 5-min health checks with webhook alerts |

---

## 12. Disaster Recovery

| Metric | Value |
|--------|-------|
| RTO | 30 minutes (full rebuild from scripts) |
| RPO | 24 hours (daily memory.json backup) |

**Recovery procedure:**
1. `make provision` — new VPS (5 min)
2. `make setup` — bootstrap server (5 min)
3. `make deploy` — deploy app (5 min)
4. `make ssl` — TLS certificate (5 min)
5. Restore latest backup from local/offsite copy
6. Register cron jobs (backup + uptime monitor)

See `docs/manuals/DR-PLAN.md` for detailed recovery steps.

---

## 13. Cost

| Resource | Provider | Monthly Cost |
|----------|----------|-------------|
| VPS (1 vCPU, 1GB RAM) | Vultr | ~$6 |
| Domain DNS | Existing | $0 |
| SSL certificate | Let's Encrypt | $0 |
| Google API usage | Google Cloud | $0 (free tier) |
| **Total** | | **~$6/month** |

---

## 14. Common Operations

```bash
# Deploy latest code
make deploy

# SSH to server
ssh deploy@anny.membies.com

# Check container status
ssh deploy@anny.membies.com "cd /opt/anny && docker compose ps"

# View container logs
ssh deploy@anny.membies.com "docker logs anny-anny-1 --tail 50"

# Restart container
ssh deploy@anny.membies.com "cd /opt/anny && docker compose restart"

# Manual backup
ssh deploy@anny.membies.com "/opt/anny/scripts/backup.sh"

# Run smoke test
ANNY_BASE_URL=https://anny.membies.com scripts/smoke_test.sh

# Rebuild from scratch
ssh deploy@anny.membies.com "cd /opt/anny && docker compose down && docker compose build && docker compose up -d"
```
