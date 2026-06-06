#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

ENGINE_DIR="$ROOT_DIR/engine"
WEBAPP_DIR="$ROOT_DIR/webapp"

if [ ! -d "$WEBAPP_DIR/db" ]; then
    echo "Creating db directory..."
    mkdir -p "$WEBAPP_DIR/db"
fi

if [ ! -f "$WEBAPP_DIR/db/users.db" ]; then
    echo "Creating users.db..."
    touch "$WEBAPP_DIR/db/users.db"
fi

PYTHON_PID=""

cleanup() {
  echo ""
  echo "Stopping Python backend..."

  if [[ -n "$PYTHON_PID" ]] && kill -0 "$PYTHON_PID" 2>/dev/null; then
    kill "$PYTHON_PID" 2>/dev/null || true
    wait "$PYTHON_PID" 2>/dev/null || true
  fi
}

trap cleanup EXIT INT TERM

echo "Starting Python backend..."

cd "$ENGINE_DIR"

if ! command -v python3.14 >/dev/null 2>&1; then
  echo "Python 3.14.3 or newer is required but python3.14 was not found."
  exit 1
fi

if [[ ! -d ".venv" ]]; then
  echo "Creating Python virtual environment with Python 3.14..."
  python3.14 -m venv .venv
fi

source "$ENGINE_DIR/.venv/bin/activate"

python_version="$(python -c 'import sys; print(".".join(map(str, sys.version_info[:3])))')"
echo "Using Python $python_version"

echo "Installing Python dependencies..."
python -m pip install -r "$ENGINE_DIR/requirements.txt"

cd "$ENGINE_DIR/src"

python -m gunicorn -w 4 -b 127.0.0.1:5000 main.communication.komunikacja:app &

PYTHON_PID=$!

echo "Python backend started with PID $PYTHON_PID"
echo "Waiting for Python backend..."

for i in {1..30}; do
  if ! kill -0 "$PYTHON_PID" 2>/dev/null; then
    echo "Python backend stopped unexpectedly."
    exit 1
  fi

  if timeout 1 bash -c "</dev/tcp/127.0.0.1/5000" 2>/dev/null; then
    echo "Python backend is running on http://127.0.0.1:5000"
    break
  fi

  sleep 1
done

echo "Starting Java/Spring server..."

cd "$WEBAPP_DIR"

./gradlew bootRun --args="--game.state-service.url=http://127.0.0.1:5000/api/neuroshima"