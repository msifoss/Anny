#!/usr/bin/env bash
# ============================================================================
# Anny — Server Setup
# Bootstraps a fresh Ubuntu VPS with Docker, nginx, UFW, fail2ban
# ============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

CONFIG_GET="${SCRIPT_DIR}/config-get"
SSH_KEY=$(python3 "$CONFIG_GET" deploy.ssh_key | sed "s|~|$HOME|")
DOMAIN=$(python3 "$CONFIG_GET" deploy.domain)

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
info "Server IP: ${SERVER_IP}"

SSH_OPTS="-o StrictHostKeyChecking=accept-new -o ConnectTimeout=10"

remote() {
    # shellcheck disable=SC2086
    ssh $SSH_OPTS -i "$SSH_KEY" "root@${SERVER_IP}" "$@"
}

# --- Wait for SSH ---
info "Waiting for SSH..."
for i in $(seq 1 30); do
    if remote "echo ok" >/dev/null 2>&1; then
        ok "SSH connected"
        break
    fi
    [[ $i -eq 30 ]] && fail "SSH connection timed out"
    sleep 5
done

# --- System update & packages ---
info "Updating system and installing packages..."
remote "DEBIAN_FRONTEND=noninteractive apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get upgrade -y -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y -qq \
        ca-certificates curl gnupg jq nginx certbot python3-certbot-nginx ufw fail2ban"
ok "Base packages installed"

# --- Install Docker from official repo ---
info "Installing Docker..."
remote "install -m 0755 -d /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc && \
    chmod a+r /etc/apt/keyrings/docker.asc && \
    echo \"deb [arch=\$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \$(. /etc/os-release && echo \$VERSION_CODENAME) stable\" > /etc/apt/sources.list.d/docker.list && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y -qq docker-ce docker-ce-cli containerd.io docker-compose-plugin"
ok "Docker installed"

# --- Deploy user ---
info "Creating deploy user..."
remote "id deploy >/dev/null 2>&1 || useradd -m -s /bin/bash deploy && \
    mkdir -p /home/deploy/.ssh && \
    cp /root/.ssh/authorized_keys /home/deploy/.ssh/authorized_keys && \
    chown -R deploy:deploy /home/deploy/.ssh && \
    chmod 700 /home/deploy/.ssh && \
    chmod 600 /home/deploy/.ssh/authorized_keys && \
    usermod -aG docker deploy"
ok "Deploy user created"

# --- Scoped sudoers ---
info "Configuring sudoers..."
remote "cat > /etc/sudoers.d/anny << 'SUDOERS'
deploy ALL=(ALL) NOPASSWD: /usr/sbin/nginx -t
deploy ALL=(ALL) NOPASSWD: /usr/bin/systemctl reload nginx
deploy ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart nginx
deploy ALL=(ALL) NOPASSWD: /usr/bin/certbot *
deploy ALL=(ALL) NOPASSWD: /usr/bin/cp /tmp/anny-https.conf /etc/nginx/sites-enabled/anny.conf
SUDOERS
chmod 440 /etc/sudoers.d/anny"
ok "Sudoers configured"

# --- App directories ---
info "Creating app directories..."
remote "mkdir -p /opt/anny/secrets && \
    chown -R deploy:deploy /opt/anny && \
    chmod 700 /opt/anny/secrets && \
    mkdir -p /var/www/certbot/.well-known/acme-challenge"
ok "Directories created"

# --- UFW ---
info "Configuring firewall..."
remote "ufw --force reset && \
    ufw default deny incoming && \
    ufw default allow outgoing && \
    ufw limit 22/tcp && \
    ufw allow 80/tcp && \
    ufw allow 443/tcp && \
    ufw --force enable"
ok "UFW configured"

# --- Nginx ---
info "Configuring nginx..."
remote "rm -f /etc/nginx/sites-enabled/default"

# Upload nginx defaults (gzip already enabled in nginx.conf)
remote "cat > /etc/nginx/conf.d/anny-defaults.conf << 'NGINX_DEFAULTS'
server_tokens off;

gzip_vary on;
gzip_proxied any;
gzip_comp_level 6;
gzip_types text/plain text/css application/json application/javascript text/xml;

client_max_body_size 1m;
NGINX_DEFAULTS"

# Upload HTTP site config
# shellcheck disable=SC2086
scp $SSH_OPTS -i "$SSH_KEY" "${PROJECT_DIR}/deploy/nginx-http.conf" \
    "root@${SERVER_IP}:/etc/nginx/sites-enabled/anny.conf"

# Ensure sites-enabled is included
remote "grep -q 'sites-enabled' /etc/nginx/nginx.conf || \
    sed -i '/http {/a\\    include /etc/nginx/sites-enabled/*.conf;' /etc/nginx/nginx.conf"

remote "nginx -t && systemctl reload nginx"
ok "Nginx configured"

# --- Fail2ban ---
info "Configuring fail2ban..."
remote "cat > /etc/fail2ban/jail.d/anny-sshd.conf << 'F2B'
[sshd]
enabled = true
port = ssh
filter = sshd
maxretry = 5
bantime = 3600
findtime = 600
F2B
systemctl enable fail2ban && systemctl restart fail2ban"
ok "Fail2ban configured"

# --- Enable certbot timer ---
remote "systemctl enable certbot.timer 2>/dev/null || true"
ok "Certbot timer enabled"

# --- Start Docker ---
remote "systemctl enable docker && systemctl start docker"
ok "Docker enabled"

echo ""
echo "============================================"
echo "  Server Setup Complete"
echo "  IP     : ${SERVER_IP}"
echo "  Domain : ${DOMAIN}"
echo "============================================"
echo ""
echo "Next: make deploy"
