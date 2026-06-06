#!/usr/bin/env bash
set -e

if ! command -v docker &> /dev/null; then
    echo "Błąd: Docker nie jest zainstalowany. Musisz zainstalować Dockera, aby uruchomić skrypt."
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [ ! -d "log" ]; then
    echo "Creating log directory..."
    mkdir log
fi

if [ ! -d "webapp/db" ]; then
    echo "Creating db directory..."
    mkdir -p webapp/db
fi

if [ ! -f "webapp/db/users.db" ]; then
    echo "Creating users.db..."
    touch webapp/db/users.db
fi

echo "Building and starting Docker containers..."
docker compose up -d --build
echo "Backend services have been started in the background."
echo "You can view logs using: docker compose logs -f"
