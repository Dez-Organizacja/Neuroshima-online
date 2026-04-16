#!/usr/bin/env bash
set -euo pipefail

HOST="${HOST:-localhost}"
PORT="${PORT:-5173}"
OPEN_BROWSER="${OPEN_BROWSER:-false}"

if [ ! -d node_modules ]; then
  echo "[run.sh] Brak node_modules, uruchamiam npm install..."
  npm install
fi

echo "[run.sh] Start dev: host=${HOST}, port=${PORT}, open=${OPEN_BROWSER}"

declare -a PIDS=()

cleanup() {
  echo
  echo "[run.sh] Zatrzymuje procesy..."

  for pid in "${PIDS[@]:-}"; do
    if kill -0 "$pid" 2>/dev/null; then
      kill "$pid" 2>/dev/null || true
    fi
  done

  wait 2>/dev/null || true
}

trap cleanup EXIT INT TERM

npm run dev:watch &
PIDS+=("$!")

npx browser-sync start \
  --server . \
  --files "dist/**/*.js,index.html,styles.css" \
  --host "$HOST" \
  --port "$PORT" \
  $( [ "$OPEN_BROWSER" = "true" ] && echo "--open" || echo "--no-open" ) &
PIDS+=("$!")

wait

