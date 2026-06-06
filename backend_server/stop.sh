#!/usr/bin/env bash
set -e

if ! command -v docker &> /dev/null; then
    echo "Błąd: Docker nie jest zainstalowany. Musisz zainstalować Dockera, aby uruchomić skrypt."
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
echo "Stopping Docker containers..."
docker compose down
echo "Backend services have been stopped."
