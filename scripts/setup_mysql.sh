#!/usr/bin/env bash
# setup_mysql.sh - Mock installation and configuration of MySQL.
# Usage: bash setup_mysql.sh <machine_name>

set -euo pipefail

MACHINE_NAME="${1:-unknown}"

log() {
    local level="$1"; shift
    local msg="$*"
    local timestamp
    timestamp="$(date '+%Y-%m-%d %H:%M:%S')"
    echo "${timestamp}  [${level}]  [${MACHINE_NAME}] ${msg}"
}

log "INFO " "MySQL setup script started."

log "INFO " "Simulating: installing mysql-server..."
sleep 0.5
log "INFO " "MySQL installed (mock)."

log "INFO " "Simulating: securing MySQL installation..."
sleep 0.3
log "INFO " "MySQL secured (mock)."

log "INFO " "Simulating: enabling mysql service..."
sleep 0.2
log "INFO " "MySQL service enabled and started (mock)."

log "INFO " "MySQL setup complete."
