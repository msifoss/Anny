#!/usr/bin/env bash
# ============================================================================
# Anny — Backup
# Backs up memory.json from the Docker volume to /opt/anny/backups/
# Retains the last 7 days of backups.
#
# Usage:  /opt/anny/scripts/backup.sh
# Cron:   0 2 * * * /opt/anny/scripts/backup.sh >> /var/log/anny-backup.log 2>&1
# ============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Read config from config.yaml if available, otherwise use defaults
CONFIG_GET="${SCRIPT_DIR}/config-get"
if [[ -f "${PROJECT_DIR}/config.yaml" ]] && command -v python3 >/dev/null 2>&1; then
    BACKUP_DIR=$(python3 "$CONFIG_GET" backup.dir)
    CONTAINER_NAME=$(python3 "$CONFIG_GET" backup.container_name)
    MEMORY_PATH=$(python3 "$CONFIG_GET" backup.memory_path)
    RETENTION_DAYS=$(python3 "$CONFIG_GET" backup.retention_days)
else
    # Fallback defaults (VPS standalone or no Python)
    BACKUP_DIR="/opt/anny/backups"
    CONTAINER_NAME=$(docker ps --filter "name=anny" --format "{{.Names}}" | head -1)
    CONTAINER_NAME="${CONTAINER_NAME:-anny-anny-1}"
    MEMORY_PATH="/home/anny/.anny/memory.json"
    RETENTION_DAYS=7
fi

ts() { date "+%Y-%m-%d %H:%M:%S"; }
info()  { printf "[%s] → %s\n" "$(ts)" "$*"; }
ok()    { printf "[%s] ✓ %s\n" "$(ts)" "$*"; }
fail()  { printf "[%s] ✗ %s\n" "$(ts)" "$*" >&2; exit 1; }

# --- Ensure backup directory exists ---
mkdir -p "$BACKUP_DIR"

# --- Check container is running ---
if ! docker inspect "$CONTAINER_NAME" >/dev/null 2>&1; then
    fail "Container ${CONTAINER_NAME} not found. Is Anny running?"
fi

# --- Copy memory.json from container ---
TIMESTAMP=$(date "+%Y%m%d-%H%M%S")
BACKUP_FILE="${BACKUP_DIR}/memory-${TIMESTAMP}.json"

if docker cp "${CONTAINER_NAME}:${MEMORY_PATH}" "$BACKUP_FILE" 2>/dev/null; then
    ok "Backed up memory.json → $(basename "$BACKUP_FILE")"
else
    # memory.json may not exist yet (fresh install)
    info "No memory.json found in container (fresh install?) — skipping"
    exit 0
fi

# --- Clean up old backups ---
DELETED=0
if [[ -d "$BACKUP_DIR" ]]; then
    while IFS= read -r old_file; do
        rm -f "$old_file"
        DELETED=$((DELETED + 1))
    done < <(find "$BACKUP_DIR" -name "memory-*.json" -mtime "+${RETENTION_DAYS}" -type f 2>/dev/null)
fi

if [[ $DELETED -gt 0 ]]; then
    info "Cleaned up ${DELETED} backup(s) older than ${RETENTION_DAYS} days"
fi

ok "Backup complete"
