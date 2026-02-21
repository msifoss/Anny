#!/usr/bin/env bash
# ============================================================================
# Anny — Uptime Monitor
# Cron-based health check with state tracking and webhook alerting.
#
# Usage:  */5 * * * * /opt/anny/scripts/uptime_monitor.sh
#
# Environment variables (optional):
#   ANNY_HEALTH_URL    — Override health endpoint (default: https://anny.membies.com/health)
#   ALERT_WEBHOOK_URL  — Webhook to POST on status transitions (e.g., Slack/Discord)
# ============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Read config from config.yaml if available, otherwise use default
if [[ -f "${PROJECT_DIR}/config.yaml" ]] && command -v python3 >/dev/null 2>&1; then
    DEFAULT_URL=$(python3 "${SCRIPT_DIR}/config-get" monitoring.health_url 2>/dev/null || echo "https://anny.membies.com/health")
else
    DEFAULT_URL="https://anny.membies.com/health"
fi
HEALTH_URL="${ANNY_HEALTH_URL:-$DEFAULT_URL}"
STATE_FILE="/tmp/anny-uptime-state"
TIMEOUT=10

ts() { date "+%Y-%m-%d %H:%M:%S"; }

# --- Check health ---
HTTP_CODE=$(curl -sf -o /dev/null -w "%{http_code}" --max-time "$TIMEOUT" "$HEALTH_URL" 2>/dev/null || echo "000")

if [[ "$HTTP_CODE" == "200" ]]; then
    CURRENT="UP"
else
    CURRENT="DOWN"
fi

# --- Read previous state ---
PREVIOUS="UNKNOWN"
if [[ -f "$STATE_FILE" ]]; then
    PREVIOUS=$(cat "$STATE_FILE")
fi

# --- Write current state ---
echo "$CURRENT" > "$STATE_FILE"

# --- Alert on transitions ---
send_alert() {
    local message="$1"
    if [[ -n "${ALERT_WEBHOOK_URL:-}" ]]; then
        curl -sf -X POST -H "Content-Type: application/json" \
            -d "{\"text\": \"$message\"}" \
            --max-time 10 \
            "$ALERT_WEBHOOK_URL" >/dev/null 2>&1 || true
    fi
}

TRANSITION="${PREVIOUS}_${CURRENT}"

if [[ "$TRANSITION" == "UP_DOWN" || "$TRANSITION" == "UNKNOWN_DOWN" ]]; then
    echo "[$(ts)] ALERT: Anny is DOWN (HTTP $HTTP_CODE)"
    send_alert "[DOWN] Anny is DOWN - health check returned HTTP $HTTP_CODE"
elif [[ "$TRANSITION" == "DOWN_UP" ]]; then
    echo "[$(ts)] RECOVERY: Anny is back UP"
    send_alert "[UP] Anny is back UP - health check recovered"
elif [[ "$TRANSITION" == "DOWN_DOWN" ]]; then
    echo "[$(ts)] STILL DOWN (HTTP $HTTP_CODE) - suppressing repeat alert"
fi
# UP_UP and UNKNOWN_UP: no action needed
