# Infrastructure Playbook

**Project:** Anny
**Last updated:** 2026-02-17

---

## Architecture

```
Internet → Cloudflare DNS → Vultr VPS (149.xxx.xxx.xxx)
                              ├── nginx (reverse proxy, TLS)
                              │     ├── Port 80 → 301 redirect to HTTPS
                              │     └── Port 443 → proxy_pass 127.0.0.1:8000
                              └── Docker
                                    └── anny container (uvicorn, port 8000)
                                          ├── FastAPI app (REST + MCP)
                                          └── Service account key (mounted read-only)
```

## Components

| Component | Version | Config |
|-----------|---------|--------|
| OS | Ubuntu (Vultr) | `scripts/server-setup.sh` |
| Docker | Latest | Installed via server-setup |
| nginx | System package | `deploy/nginx-https.conf` |
| certbot | System package | Let's Encrypt, auto-renewal |
| UFW | System package | 22, 80, 443 only |
| fail2ban | System package | SSH protection |
| Python | 3.12-slim | `Dockerfile` base image |
| uvicorn | >=0.34.0 | ASGI server |

## Deployment Scripts

| Script | Purpose | Command |
|--------|---------|---------|
| `scripts/server-provision.sh` | Create Vultr VPS + DNS | `make provision` |
| `scripts/server-setup.sh` | Bootstrap Docker, nginx, security | `make setup` |
| `scripts/deploy.sh` | Rsync code, build, restart, health check | `make deploy` |
| `scripts/ssl-setup.sh` | Certbot SSL certificate | `make ssl-setup` |

## Secrets

| Secret | Location (VPS) | Location (Dev) |
|--------|---------------|----------------|
| Service account key | `/opt/anny/secrets/service-account.json` | Local `.env` path |
| Environment config | `/opt/anny/.env` | `.env` in project root |
| SSH deploy key | `~deploy/.ssh/authorized_keys` | `~/.ssh/webengine_deploy` |

## Monitoring

| Check | Method | Frequency |
|-------|--------|-----------|
| Container health | Docker HEALTHCHECK | Every 30s |
| nginx access logs | `/var/log/nginx/anny.access.log` | Continuous |
| nginx error logs | `/var/log/nginx/anny.error.log` | Continuous |
| Container logs | `docker compose logs` | On demand |

## Common Operations

```bash
# Deploy latest code
make deploy

# SSH to server
ssh deploy@anny.membies.com

# Check container status
ssh deploy@anny.membies.com "cd /opt/anny && docker compose ps"

# View container logs
ssh deploy@anny.membies.com "cd /opt/anny && docker compose logs --tail 50"

# Restart container
ssh deploy@anny.membies.com "cd /opt/anny && docker compose restart"

# Rebuild from scratch
ssh deploy@anny.membies.com "cd /opt/anny && docker compose down && docker compose build && docker compose up -d"
```

## Cost

| Resource | Provider | Monthly Cost |
|----------|----------|-------------|
| VPS (1 vCPU, 1GB RAM) | Vultr | ~$6 |
| Domain DNS | Existing | $0 |
| SSL certificate | Let's Encrypt | $0 |
| Google API usage | Google Cloud | $0 (free tier) |
| **Total** | | **~$6/month** |
