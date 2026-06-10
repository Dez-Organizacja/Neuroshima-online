#!/usr/bin/env bash
# =============================================================================
# Uruchomienie backendu w trybie PRODUKCYJNYM.
#
# Co robi ten skrypt:
#   1. sprawdza wymagania (docker),
#   2. tworzy katalogi log/ i webapp/db/ oraz pusta baze users.db,
#   3. buduje i uruchamia kontenery z profilem Spring 'prod'
#      (auth.registration.enabled=false, captcha.required=false domyslnie, CORS = https://heuroshimanex.pl,
#       engine niewystawiony, webapp tylko na 127.0.0.1:8080 za nginx).
#
# Po uruchomieniu skonfiguruj nginx + TLS wg deploy/PRODUCTION.md
# =============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# --- 1. Wymagania ---
if ! command -v docker >/dev/null 2>&1; then
    echo "Blad: Docker nie jest zainstalowany." >&2
    exit 1
fi

if ! docker compose version >/dev/null 2>&1; then
    echo "Blad: 'docker compose' (plugin v2) nie jest dostepny." >&2
    exit 1
fi

# Captcha jest self-hosted (obrazkowa) - nie wymaga zadnych sekretow.
# Plik .env jest opcjonalny; jesli istnieje, docker compose wczyta go samodzielnie.

# --- 2. Katalogi i baza ---
[ -d "log" ] || { echo "Tworze katalog log/..."; mkdir -p log; }
[ -d "webapp/db" ] || { echo "Tworze katalog webapp/db/..."; mkdir -p webapp/db; }
[ -f "webapp/db/users.db" ] || { echo "Tworze pusta baze users.db..."; touch webapp/db/users.db; }

# --- 3. Uruchomienie ---
echo "Buduje i uruchamiam kontenery (profil prod)..."
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build

echo ""
echo "Gotowe. Backend slucha lokalnie na 127.0.0.1:8080 (engine niewystawiony)."
echo "Logi:    docker compose logs -f"
echo "Status:  curl http://127.0.0.1:8080/api/health"
echo ""
echo "Nastepny krok: nginx + certyfikat TLS -> zobacz deploy/PRODUCTION.md"
