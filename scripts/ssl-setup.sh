#!/usr/bin/env bash
# ============================================================================
# Anny — SSL Setup
# Obtains Let's Encrypt certificate and switches nginx to HTTPS
# ============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

CONFIG_GET="${SCRIPT_DIR}/config-get"
SSH_KEY=$(python3 "$CONFIG_GET" deploy.ssh_key | sed "s|~|$HOME|")
DOMAIN=$(python3 "$CONFIG_GET" deploy.domain)
EMAIL="${CERTBOT_EMAIL:-}"

# --- Helpers ---
info()  { printf "\033[34m→\033[0m %s\n" "$*"; }
ok()    { printf "\033[32m✓\033[0m %s\n" "$*"; }
fail()  { printf "\033[31m✗\033[0m %s\n" "$*" >&2; exit 1; }

# --- Preflight ---
[[ -z "$EMAIL" ]] && fail "Set CERTBOT_EMAIL env var (e.g. export CERTBOT_EMAIL=you@example.com)"

# --- Resolve IP ---
if [[ -f "${PROJECT_DIR}/.server-ip" ]]; then
    SERVER_IP=$(cat "${PROJECT_DIR}/.server-ip")
else
    SERVER_IP=$(dig +short "$DOMAIN" | head -1)
fi
[[ -z "$SERVER_IP" ]] && fail "Cannot determine server IP"
info "Server IP: ${SERVER_IP}"

SSH_OPTS="-o StrictHostKeyChecking=accept-new -o ConnectTimeout=10"

remote() {
    # shellcheck disable=SC2086
    ssh $SSH_OPTS -i "$SSH_KEY" "deploy@${SERVER_IP}" "$@"
}

# --- Verify DNS ---
info "Verifying DNS resolution..."
DNS_IP=$(dig +short "$DOMAIN" | head -1)
if [[ "$DNS_IP" != "$SERVER_IP" ]]; then
    fail "DNS mismatch: ${DOMAIN} resolves to ${DNS_IP}, expected ${SERVER_IP}"
fi
ok "DNS verified: ${DOMAIN} → ${SERVER_IP}"

# --- Obtain certificate ---
info "Requesting certificate from Let's Encrypt..."
remote "sudo certbot certonly \
    --webroot \
    --webroot-path /var/www/certbot \
    --email ${EMAIL} \
    --agree-tos \
    --no-eff-email \
    --non-interactive \
    -d ${DOMAIN}"
ok "Certificate obtained"

# --- Deploy HTTPS nginx config ---
info "Deploying HTTPS nginx config..."
# shellcheck disable=SC2086
scp $SSH_OPTS -i "$SSH_KEY" \
    "${PROJECT_DIR}/deploy/nginx-https.conf" \
    "deploy@${SERVER_IP}:/tmp/anny-https.conf"
remote "sudo cp /tmp/anny-https.conf /etc/nginx/sites-enabled/anny.conf && rm /tmp/anny-https.conf"
ok "HTTPS config deployed"

# --- Reload nginx ---
info "Testing and reloading nginx..."
remote "sudo nginx -t && sudo systemctl reload nginx"
ok "Nginx reloaded"

# --- Verify ---
info "Verifying HTTPS..."
sleep 2
HTTP_STATUS=$(curl -so /dev/null -w '%{http_code}' "https://${DOMAIN}/health" 2>/dev/null || echo "000")
if [[ "$HTTP_STATUS" == "200" ]]; then
    ok "HTTPS working — https://${DOMAIN}/health returned ${HTTP_STATUS}"
else
    fail "HTTPS verification failed (status: ${HTTP_STATUS}). Check: ssh deploy@${SERVER_IP} 'sudo nginx -t'"
fi

echo ""
echo "============================================"
echo "  SSL Setup Complete"
echo "  https://${DOMAIN}/health"
echo "============================================"
