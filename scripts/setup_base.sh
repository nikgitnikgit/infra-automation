#!/usr/bin/env bash
# setup_base.sh - Base system mock setup for a provisioned machine.
# Usage: bash setup_base.sh <machine_name>

set -euo pipefail

MACHINE_NAME="${1:-unknown}"
LOG_DIR="$(dirname "$0")/../logs"
LOG_FILE="${LOG_DIR}/provisioning.log"

mkdir -p "${LOG_DIR}"

log() {
    local level="$1"; shift
    local msg="$*"
    local timestamp
    timestamp="$(date '+%Y-%m-%d %H:%M:%S')"
    echo "${timestamp}  [${level}]  [${MACHINE_NAME}] ${msg}" | tee -a "${LOG_FILE}"
}

log "INFO " "Base setup script started."

# ── Mock: update package index ──────────────────────────────────────────
log "INFO " "Simulating: apt-get update / yum update…"
sleep 0.3
log "INFO " "Package index updated (mock)."

# ── Mock: set hostname ───────────────────────────────────────────────────
log "INFO " "Simulating: setting hostname to '${MACHINE_NAME}'…"
sleep 0.2
log "INFO " "Hostname set (mock)."

# ── Mock: configure firewall ─────────────────────────────────────────────
log "INFO " "Simulating: enabling firewall rules…"
sleep 0.2
log "INFO " "Firewall configured (mock)."

log "INFO " "Base setup complete."
