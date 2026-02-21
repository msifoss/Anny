#!/usr/bin/env bash
# ============================================================================
# Anny — Server Provisioning
# Creates a Vultr VPS and sets up DNS record for anny.membies.com
# ============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# --- Config ---
CONFIG_GET="${SCRIPT_DIR}/config-get"
PLAN=$(python3 "$CONFIG_GET" infra.vultr_plan)
REGION=$(python3 "$CONFIG_GET" infra.vultr_region)
OS_ID=$(python3 "$CONFIG_GET" infra.vultr_os_id)
LABEL=$(python3 "$CONFIG_GET" infra.vultr_label)
DOMAIN=$(python3 "$CONFIG_GET" infra.parent_domain)
SUBDOMAIN=$(python3 "$CONFIG_GET" infra.subdomain)
SSH_KEY_NAME=$(python3 "$CONFIG_GET" infra.ssh_key_name)
VULTR_API="https://api.vultr.com/v2"
POLL_INTERVAL=10
TIMEOUT=300

# --- Helpers ---
info()  { printf "\033[34m→\033[0m %s\n" "$*"; }
ok()    { printf "\033[32m✓\033[0m %s\n" "$*"; }
fail()  { printf "\033[31m✗\033[0m %s\n" "$*" >&2; exit 1; }

vultr() {
    local method="$1" endpoint="$2"
    shift 2
    curl -sf -X "$method" \
        -H "Authorization: Bearer ${VULTR_API_KEY}" \
        -H "Content-Type: application/json" \
        "${VULTR_API}${endpoint}" "$@"
}

# --- Preflight ---
[[ -z "${VULTR_API_KEY:-}" ]] && fail "VULTR_API_KEY is not set"
command -v curl >/dev/null || fail "curl is required"
command -v jq >/dev/null   || fail "jq is required"

# --- Find SSH key ---
info "Looking up SSH key '${SSH_KEY_NAME}'..."
SSH_KEY_ID=$(vultr GET /ssh-keys | jq -r --arg name "$SSH_KEY_NAME" \
    '.ssh_keys[] | select(.name == $name) | .id' | head -1)
[[ -z "$SSH_KEY_ID" ]] && fail "SSH key '${SSH_KEY_NAME}' not found on Vultr"
ok "SSH key: ${SSH_KEY_ID}"

# --- Create instance ---
info "Creating VPS (${PLAN}, ${REGION}, Ubuntu 24.04)..."
INSTANCE=$(vultr POST /instances -d "{
    \"region\": \"${REGION}\",
    \"plan\": \"${PLAN}\",
    \"os_id\": ${OS_ID},
    \"label\": \"${LABEL}\",
    \"tags\": [\"anny\"],
    \"sshkey_id\": [\"${SSH_KEY_ID}\"]
}")
INSTANCE_ID=$(echo "$INSTANCE" | jq -r '.instance.id')
[[ -z "$INSTANCE_ID" || "$INSTANCE_ID" == "null" ]] && fail "Failed to create instance: ${INSTANCE}"
ok "Instance created: ${INSTANCE_ID}"

# --- Poll until active ---
info "Waiting for instance to become active..."
ELAPSED=0
while [[ $ELAPSED -lt $TIMEOUT ]]; do
    STATUS_JSON=$(vultr GET "/instances/${INSTANCE_ID}")
    STATUS=$(echo "$STATUS_JSON" | jq -r '.instance.status')
    POWER=$(echo "$STATUS_JSON" | jq -r '.instance.power_status')
    IP=$(echo "$STATUS_JSON" | jq -r '.instance.main_ip')

    if [[ "$STATUS" == "active" && "$POWER" == "running" && "$IP" != "0.0.0.0" ]]; then
        ok "Instance active — IP: ${IP}"
        break
    fi

    printf "  status=%s power=%s ip=%s (%ds/%ds)\n" "$STATUS" "$POWER" "$IP" "$ELAPSED" "$TIMEOUT"
    sleep "$POLL_INTERVAL"
    ELAPSED=$((ELAPSED + POLL_INTERVAL))
done

[[ $ELAPSED -ge $TIMEOUT ]] && fail "Timed out waiting for instance (${TIMEOUT}s)"

# --- Create DNS record ---
info "Creating DNS A record: ${SUBDOMAIN}.${DOMAIN} → ${IP}..."
DNS_RESULT=$(vultr POST "/domains/${DOMAIN}/records" -d "{
    \"name\": \"${SUBDOMAIN}\",
    \"type\": \"A\",
    \"data\": \"${IP}\",
    \"ttl\": 300
}")
DNS_ID=$(echo "$DNS_RESULT" | jq -r '.record.id')
[[ -z "$DNS_ID" || "$DNS_ID" == "null" ]] && fail "Failed to create DNS record: ${DNS_RESULT}"
ok "DNS record created: ${DNS_ID}"

# --- Save IP ---
echo "$IP" > "${PROJECT_DIR}/.server-ip"
ok "IP saved to .server-ip"

echo ""
echo "============================================"
echo "  VPS Provisioned"
echo "  Instance ID : ${INSTANCE_ID}"
echo "  IP Address  : ${IP}"
echo "  Domain      : ${SUBDOMAIN}.${DOMAIN}"
echo "============================================"
echo ""
echo "Next: make setup"
