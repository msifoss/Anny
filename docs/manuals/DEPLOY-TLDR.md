# Anny Deploy — TLDR

One command deploys **everything**: REST API, MCP server, and health endpoint. They're all the same FastAPI process in one Docker container.

---

## What Gets Deployed

```
                    https://anny.membies.com
                              │
                           nginx (TLS)
                              │
                    Docker container (:8000)
                    ┌─────────┼─────────┐
                    │         │         │
               /api/*      /mcp     /health
              REST API   MCP Server  Health
            (X-API-Key)  (Bearer)   (no auth)
```

- **REST API** (`/api/*`) — 25 endpoints for GA4, Search Console, Tag Manager, cache, export, logs
- **MCP Server** (`/mcp`) — 26 tools for LLM clients (Claude Desktop, Claude Code, etc.)
- **Health** (`/health`) — unauthenticated monitoring endpoint

All three update simultaneously on every deploy. There is no separate MCP deploy.

---

## How to Deploy

```bash
make deploy
```

That's it. Under the hood (`scripts/deploy.sh`):

1. Rsyncs source code to VPS (`/opt/anny/`)
2. Uploads `.env` and service account key
3. Tags current running image as `anny:rollback` (safety net)
4. `docker compose build && docker compose up -d`
5. Polls `/health` every 5s for 60s
6. If health fails → **automatic rollback** to previous image
7. If health passes → runs smoke test against live domain

---

## Deploy Checklist (Quick)

```bash
# Before deploying
make test                    # 275 tests pass?
make lint                    # pylint 10/10?
git status                   # working tree clean?

# Deploy
git push origin main --tags  # push code (also triggers CI/CD)
make deploy                  # deploy to VPS

# Verify
curl https://anny.membies.com/health
```

---

## Release + Deploy (Version Bump)

When cutting a new version (e.g. v0.11.0):

```bash
# 1. Bump version
#    - pyproject.toml: version = "0.11.0"
#    - config.yaml: app.version: "0.11.0"
#    - docs/REQUIREMENTS.md: Version line

# 2. Move CHANGELOG [Unreleased] → [0.11.0] - YYYY-MM-DD

# 3. Commit, tag, push
git add -A
git commit -m "Release v0.11.0: ..."
git tag v0.11.0
git push origin main --tags

# 4. Deploy
make deploy
```

Or just ask Claude to run `/pm` and handle the release.

---

## Where It Runs

| Component | Value |
|-----------|-------|
| VPS | Vultr `vc2-1c-1gb`, 1 vCPU, 1 GB RAM, $6/month |
| Region | `ewr` (New Jersey) |
| OS | Ubuntu 24.04 |
| Domain | `anny.membies.com` |
| TLS | Let's Encrypt via certbot (auto-renew) |
| Firewall | UFW — ports 22, 80, 443 only |
| Container | Python 3.12, non-root user (`anny`, UID 1000) |
| Port | `127.0.0.1:8000` (localhost only, nginx proxies external traffic) |

---

## Auth

| Interface | Header | Value |
|-----------|--------|-------|
| REST API | `X-API-Key` | `ANNY_API_KEY` from `.env` |
| MCP Server | `Authorization` | `Bearer <ANNY_API_KEY>` |
| Health | (none) | Unauthenticated |

Same key for both. Set `ANNY_API_KEY=` (empty) to disable auth in dev.

---

## Connecting MCP Clients

### Claude Desktop

`~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "anny": {
      "type": "streamable-http",
      "url": "https://anny.membies.com/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY_HERE"
      }
    }
  }
}
```

### Claude Code

```bash
claude mcp add anny --transport http https://anny.membies.com/mcp \
  --header "Authorization: Bearer YOUR_API_KEY_HERE"
```

---

## Rollback

### Automatic (built into deploy.sh)

If the health check fails after deploy, the script automatically:
1. Stops the broken container
2. Restores the `anny:rollback` image
3. Restarts and verifies health

You don't need to do anything — it just works.

### Manual

```bash
ssh deploy@anny.membies.com
cd /opt/anny

# Check what's wrong
docker compose logs --tail 100

# Roll back
docker compose down
docker tag anny:rollback anny-anny:latest
docker compose up -d
```

---

## What Persists Across Deploys

| Persists | Replaced |
|----------|----------|
| `~/.anny/memory.json` (Docker volume) | Python source (`src/anny/`) |
| nginx config, TLS certs | `config.yaml`, `docker-compose.yml` |
| UFW/fail2ban rules | `.env`, service account key |
| Backups (`/opt/anny/backups/`) | `requirements.txt`, `pyproject.toml` |

---

## Backup

Daily cron (2 AM) runs `scripts/backup.sh`:
- Copies `memory.json` from Docker volume
- 7-day retention at `/opt/anny/backups/`
- RTO: 30 min, RPO: 24 hours

---

## CI/CD (Automatic)

Pushing to `main` triggers GitHub Actions:
1. **CI** — format check, lint, tests, pip-audit
2. **CD** (after CI passes) — SSHs to VPS, rebuilds container

`make deploy` does the same thing manually with full rsync + secrets upload.
