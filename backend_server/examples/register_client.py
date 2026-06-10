#!/usr/bin/env python3
"""Przykładowy klient rejestracji z captchą obrazkową (self-hosted).

Przepływ:
  1. GET  /api/auth/captcha            -> { "captchaId": "...", "image": "data:image/png;base64,..." }
  2. zapisz/pokaż obrazek, użytkownik przepisuje kod
  3. POST /api/auth/register           -> { username, password, captchaId, captchaAnswer }

Używa wyłącznie biblioteki standardowej (urllib) - nie wymaga instalacji niczego.

Uruchomienie:
    python3 register_client.py --base-url http://localhost:8080 --username alice
"""
import argparse
import base64
import getpass
import json
import os
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request


def _post_json(url, payload):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read() or b"{}")
    except urllib.error.HTTPError as e:
        body = e.read() or b"{}"
        try:
            return e.code, json.loads(body)
        except json.JSONDecodeError:
            return e.code, {"error": body.decode("utf-8", "replace")}


def _get_json(url):
    with urllib.request.urlopen(url) as resp:
        return json.loads(resp.read() or b"{}")


def _open_image(png_bytes):
    """Zapisuje PNG do pliku tymczasowego i próbuje otworzyć go domyślną przeglądarką."""
    fd, path = tempfile.mkstemp(suffix=".png", prefix="captcha_")
    with os.fdopen(fd, "wb") as f:
        f.write(png_bytes)
    opener = {"linux": ["xdg-open"], "darwin": ["open"], "win32": ["cmd", "/c", "start", ""]}.get(sys.platform)
    if opener:
        try:
            subprocess.Popen(opener + [path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except OSError:
            pass
    return path


def main():
    ap = argparse.ArgumentParser(description="Rejestracja konta z captchą obrazkową.")
    ap.add_argument("--base-url", default="http://localhost:8080", help="Adres backendu (bez /api).")
    ap.add_argument("--username", help="Nazwa użytkownika (jeśli pominięta - zapyta).")
    args = ap.parse_args()

    base = args.base_url.rstrip("/")
    username = args.username or input("Nazwa użytkownika: ").strip()
    password = getpass.getpass("Hasło: ")

    # 1. Pobierz wyzwanie captcha.
    challenge = _get_json(f"{base}/api/auth/captcha")
    captcha_id = challenge["captchaId"]
    header, b64 = challenge["image"].split(",", 1)  # "data:image/png;base64,...."
    png = base64.b64decode(b64)
    path = _open_image(png)
    print(f"Obrazek captcha zapisany: {path}")

    # 2. Użytkownik przepisuje kod.
    answer = input("Przepisz kod z obrazka: ").strip()

    # 3. Rejestracja.
    status, body = _post_json(f"{base}/api/auth/register", {
        "username": username,
        "password": password,
        "captchaId": captcha_id,
        "captchaAnswer": answer,
    })
    if status in (200, 201):
        print("OK - konto utworzone, możesz się zalogować.")
    else:
        print(f"Błąd ({status}): {body.get('error', body)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
