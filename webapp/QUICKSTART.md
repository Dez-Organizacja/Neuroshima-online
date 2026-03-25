# WebSocket - Szybki Start

Ten przewodnik uruchamia aktualną wersję projektu:
- backend Java w pakiecie `pl.staszic.neu`
- protokół `STARTNEWGAME` / `ENDTURN` / `ENDGAME`
- klient wyłącznie w Pythonie

## 1) Wymagania

- Java 17+
- Python 3.10+

## 2) Instalacja zależności Python

Na Linuxie (PEP 668) najbezpieczniej użyć lokalnego środowiska virtualenv:

```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

## 3) Uruchom serwer

```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp
./gradlew bootRun
```

Serwer nasłuchuje na:
- `ws://localhost:8080/ws/chat`
- `http://localhost:8080/api/websocket/stats`

## 4) Uruchom klienta Python

W nowym terminalu:

```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp/client
../.venv/bin/python websocket_client.py
```

Domyślny scenariusz klienta:
1. wysyła `STARTNEWGAME_REQUEST`
2. wysyła `ENDTURN_REQUEST`
3. wysyła `ENDGAME_REQUEST`

Przykład z parametrami:

```bash
../.venv/bin/python websocket_client.py --server ws://localhost:8080/ws/chat --player "Bot-1" --scenario "Moloch" --turn 2 --reason "Smoke test"
```

## 5) Szybki test protokołu

```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp/client
../.venv/bin/python test.py
```

## 6) Sprawdzenie logów

```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp
tail -f logs/websocket.log
```

## 7) Najczęstsze problemy

- `ModuleNotFoundError: websocket`: zainstaluj zależności przez `.venv/bin/python -m pip install -r requirements.txt`
- brak połączenia: upewnij się, że serwer działa (`./gradlew bootRun`)
- zajęty port 8080: zmień `server.port` w `application.properties`

## Następny krok

Pełna dokumentacja: `doc/README.md`

