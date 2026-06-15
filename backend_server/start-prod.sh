#!/usr/bin/env bash
# Build and start the complete production application.
#
# The frontend is built inside Docker and embedded into the Spring Boot JAR.
# Therefore an existing nginx configuration that proxies the domain to
# 127.0.0.1:8080 will automatically serve the React application instead of the
# old placeholder index.html. No manual nginx edit is required.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$SCRIPT_DIR"

say() {
    printf '%s\n' "$*"
}

fail() {
    printf 'Error: %s\n' "$*" >&2
    exit 1
}

ensure_runtime_path() {
    local path="$1"
    local kind="$2"

    if [[ "$kind" == "dir" ]]; then
        if mkdir -p "$path" 2>/dev/null; then
            return
        fi
    else
        if mkdir -p "$(dirname "$path")" 2>/dev/null && touch "$path" 2>/dev/null; then
            return
        fi
    fi

    command -v sudo >/dev/null 2>&1 \
        || fail "Cannot create $path. Extract the project as your normal user or install sudo."

    say "Requesting sudo once to repair deployment-directory permissions..."
    if [[ "$kind" == "dir" ]]; then
        sudo mkdir -p "$path"
    else
        sudo mkdir -p "$(dirname "$path")"
        sudo touch "$path"
    fi
    sudo chown -R "$(id -u):$(id -g)" "$path"
}

command -v docker >/dev/null 2>&1 || fail "Docker is not installed."
docker compose version >/dev/null 2>&1 || fail "Docker Compose v2 is not available."

# Use Docker directly when possible. If the current account cannot access the
# Docker socket, fall back to sudo instead of requiring a manual docker-group
# change.
DOCKER=(docker)
if ! docker info >/dev/null 2>&1; then
    if command -v sudo >/dev/null 2>&1 && sudo docker info >/dev/null 2>&1; then
        DOCKER=(sudo docker)
    else
        fail "Cannot access the Docker daemon. Start Docker and check permissions."
    fi
fi

ensure_runtime_path "$SCRIPT_DIR/log" dir
ensure_runtime_path "$SCRIPT_DIR/webapp/db" dir
ensure_runtime_path "$SCRIPT_DIR/webapp/db/users.db" file

say "Building the React frontend and backend containers..."
"${DOCKER[@]}" compose \
    -f docker-compose.yml \
    -f docker-compose.prod.yml \
    up -d --build --remove-orphans

say "Waiting for Spring Boot..."
ready=0
for _ in $(seq 1 60); do
    if command -v curl >/dev/null 2>&1 \
        && curl -fsS http://127.0.0.1:8080/api/health >/dev/null 2>&1; then
        ready=1
        break
    fi
    sleep 2
done

if [[ "$ready" -ne 1 ]]; then
    say "The containers started, but the health endpoint did not become ready in time."
    say "Recent logs:"
    "${DOCKER[@]}" compose \
        -f docker-compose.yml \
        -f docker-compose.prod.yml \
        logs --tail=120 webapp || true
    exit 1
fi

if command -v curl >/dev/null 2>&1; then
    homepage="$(curl -fsS http://127.0.0.1:8080/ || true)"
    if ! grep -Eq '/assets/[^" ]+\.js|type="module"' <<<"$homepage"; then
        say "Warning: the backend is healthy, but the homepage does not look like a Vite build."
        say "Run: ${DOCKER[*]} compose -f docker-compose.yml -f docker-compose.prod.yml logs webapp"
        exit 1
    fi
fi

say ""
say "Deployment complete."
say "- React frontend: embedded in the Spring Boot application"
say "- Backend:        http://127.0.0.1:8080"
say "- Health check:   http://127.0.0.1:8080/api/health"
say "- CAPTCHA:        enabled in docker-compose.prod.yml"
say ""
say "Your existing nginx proxy can continue forwarding the domain to 127.0.0.1:8080."
say "It will now receive the built React frontend instead of the placeholder HTML."
