#!/usr/bin/env bash
# ============================================================================
# Anny — Deploy
# Deploys/updates the app on the VPS
# ============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

SSH_KEY="${HOME}/.ssh/webengine_deploy"
DOMAIN="anny.membies.com"
REMOTE_DIR="/opt/anny"

# --- Helpers ---
info()  { printf "\033[34m→\033[0m %s\n" "$*"; }
ok()    { printf "\033[32m✓\033[0m %s\n" "$*"; }
fail()  { printf "\033[31m✗\033[0m %s\n" "$*" >&2; exit 1; }

# --- Resolve IP ---
if [[ -f "${PROJECT_DIR}/.server-ip" ]]; then
    SERVER_IP=$(cat "${PROJECT_DIR}/.server-ip")
else
    SERVER_IP=$(dig +short "$DOMAIN" | head -1)
fi
[[ -z "$SERVER_IP" ]] && fail "Cannot determine server IP. Run 'make provision' first."
info "Deploying to ${SERVER_IP} (${DOMAIN})"

SSH_OPTS="-o StrictHostKeyChecking=accept-new -o ConnectTimeout=10"

remote() {
    # shellcheck disable=SC2086
    ssh $SSH_OPTS -i "$SSH_KEY" "deploy@${SERVER_IP}" "$@"
}

# --- Preflight checks ---
[[ -f "${PROJECT_DIR}/.env" ]] || fail ".env file not found"

# Find service account key from .env or fallback names
SA_KEY=""
if grep -q 'GOOGLE_SERVICE_ACCOUNT_KEY_PATH' "${PROJECT_DIR}/.env"; then
    SA_KEY_NAME=$(grep 'GOOGLE_SERVICE_ACCOUNT_KEY_PATH' "${PROJECT_DIR}/.env" | head -1 | cut -d= -f2)
    [[ -f "${PROJECT_DIR}/${SA_KEY_NAME}" ]] && SA_KEY="${PROJECT_DIR}/${SA_KEY_NAME}"
fi
[[ -z "$SA_KEY" && -f "${PROJECT_DIR}/service-account-key.json" ]] && SA_KEY="${PROJECT_DIR}/service-account-key.json"
[[ -z "$SA_KEY" ]] && fail "Service account key not found (checked .env path and service-account-key.json)"
info "Using service account key: $(basename "$SA_KEY")"

# --- Sync project files ---
info "Syncing project files..."
# shellcheck disable=SC2086
rsync -az --delete \
    -e "ssh ${SSH_OPTS} -i ${SSH_KEY}" \
    --include='Dockerfile' \
    --include='docker-compose.yml' \
    --include='requirements.txt' \
    --include='pyproject.toml' \
    --include='src/***' \
    --exclude='*' \
    "${PROJECT_DIR}/" "deploy@${SERVER_IP}:${REMOTE_DIR}/"
ok "Project files synced"

# --- Upload secrets ---
info "Uploading .env..."
# shellcheck disable=SC2086
scp $SSH_OPTS -i "$SSH_KEY" \
    "${PROJECT_DIR}/.env" "deploy@${SERVER_IP}:${REMOTE_DIR}/.env"
ok ".env uploaded"

info "Uploading service account key..."
# shellcheck disable=SC2086
scp $SSH_OPTS -i "$SSH_KEY" \
    "${SA_KEY}" \
    "deploy@${SERVER_IP}:${REMOTE_DIR}/secrets/service-account.json"
remote "chmod 600 ${REMOTE_DIR}/secrets/service-account.json"
ok "Service account key uploaded"

# --- Build and start ---
info "Building and starting container..."
remote "cd ${REMOTE_DIR} && docker compose build && docker compose up -d"
ok "Container started"

# --- Health check ---
info "Waiting for health check..."
ELAPSED=0
TIMEOUT=60
while [[ $ELAPSED -lt $TIMEOUT ]]; do
    if remote "curl -sf http://localhost:8000/health" >/dev/null 2>&1; then
        ok "Health check passed"
        echo ""
        echo "============================================"
        echo "  Deploy Successful"
        echo "  http://${DOMAIN}/health"
        echo "============================================"
        echo ""
        echo "Next: make ssl-setup"
        exit 0
    fi
    sleep 5
    ELAPSED=$((ELAPSED + 5))
    printf "  waiting... (%ds/%ds)\n" "$ELAPSED" "$TIMEOUT"
done

fail "Health check failed after ${TIMEOUT}s. Check: ssh deploy@${SERVER_IP} 'cd ${REMOTE_DIR} && docker compose logs'"
