#!/usr/bin/env bash
# ============================================================================
# Anny — Deploy
# Deploys/updates the app on the VPS
# ============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

CONFIG_GET="${SCRIPT_DIR}/config-get"
SSH_KEY=$(python3 "$CONFIG_GET" deploy.ssh_key | sed "s|~|$HOME|")
DOMAIN=$(python3 "$CONFIG_GET" deploy.domain)
REMOTE_DIR=$(python3 "$CONFIG_GET" deploy.remote_dir)
HEALTH_TIMEOUT=$(python3 "$CONFIG_GET" deploy.health_check_timeout)

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
    --include='config.yaml' \
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
remote "chmod 644 ${REMOTE_DIR}/secrets/service-account.json"
ok "Service account key uploaded"

# --- Save current image for rollback ---
info "Saving current image for rollback..."
ROLLBACK_AVAILABLE=false
if remote "docker compose -f ${REMOTE_DIR}/docker-compose.yml images -q 2>/dev/null" >/dev/null 2>&1; then
    CURRENT_IMAGE=$(remote "docker compose -f ${REMOTE_DIR}/docker-compose.yml images -q 2>/dev/null | head -1")
    if [[ -n "$CURRENT_IMAGE" ]]; then
        remote "docker tag ${CURRENT_IMAGE} anny:rollback"
        ROLLBACK_AVAILABLE=true
        ok "Current image tagged as anny:rollback (${CURRENT_IMAGE:0:12})"
    else
        info "No running image found (first deploy?) — rollback not available"
    fi
else
    info "No running container found (first deploy?) — rollback not available"
fi

# --- Build and start ---
info "Building and starting container..."
remote "cd ${REMOTE_DIR} && docker compose build && docker compose up -d"
ok "Container started"

# --- Health check ---
health_check() {
    local elapsed=0
    local timeout="${HEALTH_TIMEOUT}"
    while [[ $elapsed -lt $timeout ]]; do
        if remote "curl -sf http://localhost:8000/health" >/dev/null 2>&1; then
            return 0
        fi
        sleep 5
        elapsed=$((elapsed + 5))
        printf "  waiting... (%ds/%ds)\n" "$elapsed" "$timeout"
    done
    return 1
}

info "Waiting for health check..."
if health_check; then
    ok "Health check passed"

    # --- Post-deploy smoke test ---
    if [[ -x "${SCRIPT_DIR}/smoke_test.sh" ]]; then
        info "Running post-deploy smoke test..."
        if ANNY_BASE_URL="https://${DOMAIN}" "${SCRIPT_DIR}/smoke_test.sh"; then
            ok "Smoke test passed"
        else
            echo "  (smoke test failed — deploy succeeded but some endpoints may be unhealthy)"
        fi
    fi

    echo ""
    echo "============================================"
    echo "  Deploy Successful"
    echo "  https://${DOMAIN}/health"
    echo "============================================"
    exit 0
fi

# --- Health check failed — attempt rollback ---
echo ""
if [[ "$ROLLBACK_AVAILABLE" != "true" ]]; then
    fail "Health check failed after 60s (no rollback image available). Check: ssh deploy@${SERVER_IP} 'cd ${REMOTE_DIR} && docker compose logs'"
fi

info "Health check failed — rolling back to previous image..."
remote "cd ${REMOTE_DIR} && docker compose down"
remote "docker tag anny:rollback anny-anny:latest"
remote "cd ${REMOTE_DIR} && docker compose up -d"

info "Waiting for rollback health check..."
if health_check; then
    ok "Rollback health check passed"
    echo ""
    echo "============================================"
    echo "  Deploy FAILED — Rolled Back Successfully"
    echo "  Previous version restored."
    echo "  https://${DOMAIN}/health"
    echo "============================================"
    exit 1
fi

fail "Rollback also failed. Manual intervention required: ssh deploy@${SERVER_IP} 'cd ${REMOTE_DIR} && docker compose logs'"
