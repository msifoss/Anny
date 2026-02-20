#!/usr/bin/env bash
# ============================================================================
# Anny — Uptime Monitor
# Cron-based health check with state tracking and webhook alerting.
#
# Usage:  */5 * * * * /path/to/uptime_monitor.sh
#
# Environment variables (optional):
#   ANNY_HEALTH_URL    — Override health endpoint (default: https://anny.membies.com/health)
#   ALERT_WEBHOOK_URL  — Webhook to POST on status transitions (e.g., Slack/Discord)
# ============================================================================
set -euo pipefail

HEALTH_URL="${ANNY_HEALTH_URL:-https://anny.membies.com/health}"
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

case "${PREVIOUS}->${CURRENT}" in
    UP->DOWN|UNKNOWN->DOWN)
        echo "[$(ts)] ALERT: Anny is DOWN (HTTP $HTTP_CODE)"
        send_alert "🔴 Anny is DOWN — health check returned HTTP $HTTP_CODE"
        ;;
    DOWN->UP)
        echo "[$(ts)] RECOVERY: Anny is back UP"
        send_alert "🟢 Anny is back UP — health check recovered"
        ;;
    DOWN->DOWN)
        echo "[$(ts)] STILL DOWN (HTTP $HTTP_CODE) — suppressing repeat alert"
        ;;
    *)
        # UP->UP or UNKNOWN->UP — no action needed
        ;;
esac
