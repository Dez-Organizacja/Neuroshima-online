# Important: frontend deployment

The production Docker build now compiles `frontend/` and embeds the resulting
Vite files into the Spring Boot JAR. If nginx already proxies the domain to
`127.0.0.1:8080`, no separate frontend or nginx change is required. Run
`./start-prod.sh` from the project root. See `ONE_COMMAND_DEPLOYMENT.md`.

# Wdrożenie produkcyjne — heuroshimanex.pl

Instrukcja krok po kroku: jak uruchomić backend na serwerze produkcyjnym i wygenerować
certyfikat TLS (HTTPS) dla domeny **heuroshimanex.pl**.

Architektura: internet → **nginx (TLS, port 443)** → **Spring Boot (127.0.0.1:8080)** → **engine
(tylko sieć wewnętrzna docker)**.

---

## 0. Wymagania wstępne

- Serwer z publicznym adresem IP i otwartymi portami **80** i **443**.
- Domena **heuroshimanex.pl** wskazująca rekordem **A** (i ewentualnie **AAAA**) na IP serwera.
  Sprawdź: `dig +short heuroshimanex.pl` powinno zwrócić IP serwera.
- Zainstalowane: `docker` + plugin `docker compose` v2, oraz `nginx`.

---

## 1. Captcha (self-hosted, obrazkowa)

Captcha jest generowana po stronie serwera (obrazek z kodem) i weryfikowana lokalnie — **nie
wymaga żadnych kluczy, sekretów ani usług zewnętrznych** (jak Cloudflare Turnstile). Działa dla
dowolnego klienta: przeglądarki, aplikacji Python, `curl`.

Nie trzeba więc tworzyć pliku `.env` — można od razu przejść do uruchomienia (sekcja 2).

Wymaganie captchy przy rejestracji kontroluje flaga **`captcha.required`** w
`application-prod.properties`. Domyślnie jest **`false`** (rejestracja wstecznie kompatybilna —
nie wymaga captchy), żeby istniejący klienci działali bez zmian. Endpoint
`GET /api/auth/captcha` jest dostępny niezależnie, więc klient (np. aplikacja Python) może już
dorabiać obsługę. Gdy klient będzie gotowy, ustaw `captcha.required=true` i przebuduj.

> Jeśli rejestracja ma pozostać **wyłączona** (konta zakładasz ręcznie), captcha i tak nie jest
> używana — patrz sekcja 6. Domyślnie na produkcji `auth.registration.enabled=false`.

---

## 2. Uruchomienie backendu

```bash
./start-prod.sh
```

Skrypt: sprawdzi wymagania, utworzy `log/`, `webapp/db/`, pustą `users.db`, zbuduje i uruchomi
kontenery z profilem `prod`. Po starcie:

```bash
curl http://127.0.0.1:8080/api/health     # -> {"status":"UP"}
docker compose logs -f                     # podgląd logów
```

Backend słucha tylko na `127.0.0.1:8080`; engine nie jest wystawiony na zewnątrz.

---

## 3. Konfiguracja nginx

```bash
sudo cp deploy/nginx/neuroshima-backend.conf /etc/nginx/conf.d/heuroshimanex.conf
sudo nginx -t          # test składni
sudo systemctl reload nginx
```

Na tym etapie działa już przekierowanie z portu 80 (HTTP). Blok HTTPS (443) wymaga certyfikatu —
patrz krok 4. (Linie `ssl_certificate` są na razie zakomentowane; certbot je uzupełni.)

---

## 4. Wygenerowanie certyfikatu TLS (Let's Encrypt / certbot)

### 4a. Instalacja certbota

- **Manjaro / Arch:**
  ```bash
  sudo pacman -S certbot certbot-nginx
  ```
- **Ubuntu / Debian:**
  ```bash
  sudo apt update && sudo apt install -y certbot python3-certbot-nginx
  ```

### 4b. Wygenerowanie i automatyczne wpięcie certyfikatu

```bash
sudo certbot --nginx -d heuroshimanex.pl --redirect --agree-tos -m admin@heuroshimanex.pl
```

Co się stanie:
- certbot zweryfikuje domenę (wyzwanie HTTP-01 na porcie 80),
- pobierze certyfikat do `/etc/letsencrypt/live/heuroshimanex.pl/`,
- **sam odkomentuje/wstawi** w pliku nginx linie:
  ```
  ssl_certificate     /etc/letsencrypt/live/heuroshimanex.pl/fullchain.pem;
  ssl_certificate_key /etc/letsencrypt/live/heuroshimanex.pl/privkey.pem;
  ```
- przeładuje nginx.

> Jeśli certbot nie potrafi zmodyfikować pliku automatycznie, ręcznie odkomentuj te dwie linie
> w `/etc/nginx/conf.d/heuroshimanex.conf` (sekcja `# --- TLS ---`) i wykonaj
> `sudo nginx -t && sudo systemctl reload nginx`.

### 4c. Weryfikacja automatycznego odnawiania

Certyfikat Let's Encrypt jest ważny 90 dni; certbot instaluje timer odnawiania. Sprawdź:

```bash
sudo systemctl status certbot.timer      # powinien być 'active'
sudo certbot renew --dry-run             # test odnowienia bez realnej zmiany
```

---

## 5. Weryfikacja końcowa

```bash
curl -I http://heuroshimanex.pl          # -> 301 -> https://
curl -I https://heuroshimanex.pl         # -> 200, nagłówek Strict-Transport-Security
curl https://heuroshimanex.pl/api/health # -> {"status":"UP"}
```

W przeglądarce: `https://heuroshimanex.pl` → strona powitalna, kłódka TLS, działa login.
Sprawdź też, że `http://<IP-serwera>:5000` oraz `http://<IP-serwera>:8080` **nie** odpowiadają
z zewnątrz (engine i backend nie są wystawione bezpośrednio).

---

## 6. Włączanie / wyłączanie rejestracji

Domyślnie na produkcji rejestracja jest **zablokowana** (`auth.registration.enabled=false`
w `application-prod.properties`).

- **Konta zakłada admin** (brak publicznej rejestracji): zostaw `false`. Endpoint `/api/auth/register`
  zwraca wtedy `403`, a strona `register.html` pokazuje komunikat „Rejestracja wyłączona”.
- **Publiczna rejestracja z captcha**: ustaw `auth.registration.enabled=true` w
  `application-prod.properties` i przebuduj (captcha obrazkowa jest już włączona, bez kluczy):
  ```bash
  ./start-prod.sh
  ```

---

## 7. Aktualizacja / restart / stop

```bash
./start-prod.sh                                                   # przebudowa + restart
docker compose -f docker-compose.yml -f docker-compose.prod.yml down   # zatrzymanie
docker compose -f docker-compose.yml -f docker-compose.prod.yml logs -f # logi
```

Dane użytkowników (`webapp/db/users.db`) są w wolumenie — przeżywają restart kontenerów.
