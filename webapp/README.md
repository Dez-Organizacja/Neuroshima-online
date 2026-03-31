# WebSocket Application - Neuroshima

Aplikacja czasu rzeczywistego oparta o Spring Boot (Java) i klienta Python.

## Spis treści

- [Szybki start](#szybki-start)
- [Aktualny protokół](#aktualny-protokol)
- [Uruchamianie](#uruchamianie)
- [Testowanie](#testowanie)
- [Struktura projektu](#struktura-projektu)
- [Dokumentacja](#dokumentacja)

---

## Szybki start

1) Uruchom backend:

```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp
./gradlew bootRun
```

2) W osobnym terminalu uruchom klienta:

```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp/client
python websocket_client.py
```

Domyślnie klient tylko łączy się z serwerem WebSocket i utrzymuje połączenie.

---

## Aktualny protokol

Backend działa w pakiecie `pl.staszic.neu` i obsługuje poniższe typy komunikatów JSON.

Typy `client -> server`:
- `CREATENEWROOM_REQUEST`
- `JOINROOM_REQUEST`
- `LEAVEROOM_REQUEST`
- `STARTNEWGAME_REQUEST`
- `ACTION_REQUEST`
- `ENDGAME_REQUEST`

Typy `server -> client`:
- `CONNECTION`
- `DISCONNECTION` (zdarzenie logowane po stronie serwera)
- `CREATENEWROOM_RESPONSE`
- `JOINROOM_RESPONSE`
- `LEAVEROOM_RESPONSE`
- `STARTNEWGAME_RESPONSE`
- `ENDGAME_RESPONSE`
- `ERROR`

Wspólne pola:
- `messageType`, `timestamp`, `clientId`
- wiadomości game-scoped: dodatkowo `gameId`

Walidacja po stronie serwera:
- `CREATENEWROOM_REQUEST`: wymagane `roomId`, klient nie może być już w pokoju
- `JOINROOM_REQUEST`: wymagane `roomId`, pokój musi istnieć
- `LEAVEROOM_REQUEST`: wymagane `roomId`, klient musi należeć do pokoju
- `STARTNEWGAME_REQUEST`: wymagane `roomId`, `playerId`, klient musi być członkiem pokoju
- `ACTION_REQUEST`: wymagane `playerId`, `gameId` musi istnieć; `actionData` może być JSON-em
- `ENDGAME_REQUEST`: wymagane `gameId`, `gameId` musi istnieć

Przykład `ACTION_REQUEST`:

```json
{
  "messageType": "ACTION_REQUEST",
  "clientId": "58a84c5a-ca0e-4a8d-bf04-11ae1152bdf4",
  "gameId": "8ef7dcb4-db11-4ddb-a8fc-2440391462bf",
  "playerId": "Anna",
  "actionData": {
    "action": "MOVE",
    "unitId": "u-12",
    "to": { "x": 3, "y": 5 }
  }
}
```

Pełna specyfikacja wszystkich formatów jest w `doc/README.md`.
Dla klienta Python: `doc/client/README.md`.

---

## Uruchamianie

### Wymagania

- Java 17+
- Python 3.10+

### Instalacja zależności Python

```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

### Serwer

```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp
./gradlew bootRun
```

Endpointy:

- WebSocket: `ws://localhost:8080/ws/chat`
- REST stats: `http://localhost:8080/api/websocket/stats`

### Klient (jedyna implementacja)

Jedyna implementacja klienta WebSocket jest w pliku `client/websocket_client.py`.

```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp/client
../.venv/bin/python websocket_client.py --server ws://localhost:8080/ws/chat --verbose
```

Parametry `websocket_client.py`:

- `--server` (domyślnie `ws://localhost:8080/ws/chat`)
- `-v, --verbose` (włącza bardziej szczegółowe logi)

---

## Testowanie

Build Java:

```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp
./gradlew test
```

Build dokumentacji PDF (wymaga `asciidoc2pdf`):

```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp
./gradlew docsPdf
```

---

## Struktura projektu

```text
webapp/
├── README.md
├── QUICKSTART.md
├── requirements.txt
├── src/main/java/pl/staszic/neu/
│   ├── Main.java
│   ├── WebSocketConfig.java
│   ├── WebSocketHandler.java
│   ├── WebSocketController.java
│   └── messages/
│       ├── WebSocketMessage.java
│       ├── GameScopedWebSocketMessage.java
│       ├── Room.java
│       ├── CreateNewRoomRequest.java
│       ├── CreateNewRoomResponse.java
│       ├── JoinRoomRequest.java
│       ├── JoinRoomResponse.java
│       ├── LeaveRoomRequest.java
│       ├── LeaveRoomResponse.java
│       ├── StartNewGameRequest.java
│       ├── StartNewGameResponse.java
│       ├── ActionRequest.java
│       ├── EndGameRequest.java
│       └── EndGameResponse.java
├── client/
│   ├── websocket_client.py
│   └── test.py
└── doc/
    ├── INDEX.md
    └── README.md
```

---

## Dokumentacja

- Szybki przewodnik: `QUICKSTART.md`
- Pełna dokumentacja: `doc/README.md`
- Dokumentacja klienta: `doc/client/README.md`
- Indeks dokumentacji: `doc/INDEX.md`

---

## Rozwiązywanie problemów

- `ModuleNotFoundError: websocket`: zainstaluj zależności z `requirements.txt`
- Brak połączenia: sprawdź, czy backend działa (`./gradlew bootRun`)
- Port 8080 zajęty: zmień `server.port` lub zatrzymaj proces zajmujący port

Szczegóły w: `doc/README.md`

---

## 📚 Dokumentacja

- **[QUICKSTART.md](QUICKSTART.md)** - 5 minut do pracy
- **[doc/INDEX.md](doc/INDEX.md)** - Punkt wejścia
- **[doc/README.md](doc/README.md)** - Pełna dokumentacja
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Podsumowanie

---

## 🎓 Nauczanie

Kod jest dobrze skomentowany:

**Java:**
- `WebSocketHandler.java` - Obsługa zdarzeń WebSocket
- `WebSocketMessage.java` - Format komunikatów
- `logback.xml` - Konfiguracja logowania

**Python:**
- `websocket_client.py` - Klient utrzymujący połączenie WebSocket
- `test.py` - Test smoke

---

## 🚀 Następne kroki

1. Przeczytaj: [QUICKSTART.md](QUICKSTART.md)
2. Uruchom serwer: `./gradlew bootRun`
3. Uruchom klienta: `python websocket_client.py`
4. Czytaj dokumentację: [doc/INDEX.md](doc/INDEX.md)

---

## 📊 Statystyki

```
Java:
  - WebSocketHandler.java: obsluga request/response
  - Komunikaty: baza + klasy STARTNEWGAME/ENDGAME
  - Logback.xml: 46 linii

Python:
  - websocket_client.py: klient CLI utrzymujący połączenie
  - test.py: prosty test end-to-end

Dokumentacja:
  - README.md
  - QUICKSTART.md
  - IMPLEMENTATION_SUMMARY.md
```

---

## 📄 Licencja

Część projektu Neuroshima - 2026

---

## 🎉 Uwagi

> "Całą aplikację można uruchomić w 5 minut bez żadnych problemów." - Instrukcja QUICKSTART

**Zacznij tutaj:** [QUICKSTART.md](QUICKSTART.md)

```bash
# W jednej linijce:
./gradlew bootRun & sleep 2 && cd client && python websocket_client.py --server ws://localhost:8080/ws/chat
```

---

**Happy WebSocketing! 🚀**

