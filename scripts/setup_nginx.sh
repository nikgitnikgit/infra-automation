#!/usr/bin/env bash
# setup_nginx.sh - Mock installation and configuration of Nginx.
# Usage: bash setup_nginx.sh <machine_name>

set -euo pipefail

MACHINE_NAME="${1:-unknown}"

log() {
    local level="$1"; shift
    local msg="$*"
    local timestamp
    timestamp="$(date '+%Y-%m-%d %H:%M:%S')"
    echo "${timestamp}  [${level}]  [${MACHINE_NAME}] ${msg}"
}

log "INFO " "Nginx setup script started."

if command -v nginx &>/dev/null; then
    log "INFO " "Nginx is already installed - skipping installation."
else
    log "INFO " "Simulating: installing nginx..."
    sleep 0.5
    log "INFO " "Nginx installed (mock)."
fi

log "INFO " "Simulating: enabling nginx service..."
sleep 0.2
log "INFO " "Nginx service enabled and started (mock)."

log "INFO " "Simulating: writing /etc/nginx/nginx.conf..."
sleep 0.2
log "INFO " "Nginx configuration written (mock)."

log "INFO " "Nginx setup complete."
