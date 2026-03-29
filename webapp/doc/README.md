# Dokumentacja Aplikacji WebSocket - Neuroshima

## Spis tresci
1. Przeglad
2. Architektura
3. Instalacja
4. Uruchamianie
5. Protokol komunikatow (pelny)
6. Klient Python
7. Testowanie
8. Logowanie
9. Troubleshooting

---

## 1. Przeglad

Aplikacja sklada sie z:
- serwera WebSocket w Spring Boot
- klienta Python
- endpointu REST do statystyk polaczen

Backend obsluguje protokol pokoj + gra:
- `CREATENEWROOM` (request/response)
- `JOINROOM` (request/response)
- `LEAVEROOM` (request/response)
- `STARTNEWGAME` (request/response)
- `ACTION` (request)
- `ENDTURN` (request/response)
- `ENDGAME` (request/response)
- `ERROR` (server -> client)

---

## 2. Architektura

### Java backend

Kod backendu znajduje sie w pakiecie `pl.staszic.neu`.

Najwazniejsze klasy:
- `src/main/java/pl/staszic/neu/Main.java`
- `src/main/java/pl/staszic/neu/WebSocketConfig.java`
- `src/main/java/pl/staszic/neu/WebSocketHandler.java`
- `src/main/java/pl/staszic/neu/WebSocketController.java`

Hierarchia komunikatow:
- `src/main/java/pl/staszic/neu/messages/WebSocketMessage.java`
- `src/main/java/pl/staszic/neu/messages/GameScopedWebSocketMessage.java`
- `src/main/java/pl/staszic/neu/messages/CreateNewRoomRequest.java`
- `src/main/java/pl/staszic/neu/messages/CreateNewRoomResponse.java`
- `src/main/java/pl/staszic/neu/messages/JoinRoomRequest.java`
- `src/main/java/pl/staszic/neu/messages/JoinRoomResponse.java`
- `src/main/java/pl/staszic/neu/messages/LeaveRoomRequest.java`
- `src/main/java/pl/staszic/neu/messages/LeaveRoomResponse.java`
- `src/main/java/pl/staszic/neu/messages/StartNewGameRequest.java`
- `src/main/java/pl/staszic/neu/messages/StartNewGameResponse.java`
- `src/main/java/pl/staszic/neu/messages/ActionRequest.java`
- `src/main/java/pl/staszic/neu/messages/EndTurnRequest.java`
- `src/main/java/pl/staszic/neu/messages/EndTurnResponse.java`
- `src/main/java/pl/staszic/neu/messages/EndGameRequest.java`
- `src/main/java/pl/staszic/neu/messages/EndGameResponse.java`

### Python client

- `client/websocket_client.py` - jedyna implementacja klienta WebSocket
- szczegolowy opis request/response i flow: `doc/client/README.md`

---

## 3. Instalacja

### Wymagania
- Java 17+
- Python 3.10+

### Python dependencies

Dla Linuxa (PEP 668) zalecane jest virtualenv:

```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

---

## 4. Uruchamianie

### Start serwera

```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp
./gradlew bootRun
```

Serwer udostepnia:
- WebSocket: `ws://localhost:8080/ws/chat`
- REST stats: `http://localhost:8080/api/websocket/stats`

### Start klienta

```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp/client
../.venv/bin/python websocket_client.py --server ws://localhost:8080/ws/chat
```

Tryb verbose:

```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp/client
../.venv/bin/python websocket_client.py --server ws://localhost:8080/ws/chat --verbose
```

---

## 5. Protokol komunikatow (pelny)

### 5.1 Pola wspolne

Wspolne pola (`WebSocketMessage`):
- `messageType`
- `timestamp`
- `clientId`

Wiadomosci game-scoped (`GameScopedWebSocketMessage`) dodatkowo:
- `gameId`

### 5.2 Typy komunikatow

`client -> server`:
- `CREATENEWROOM_REQUEST`
- `JOINROOM_REQUEST`
- `LEAVEROOM_REQUEST`
- `STARTNEWGAME_REQUEST`
- `ACTION_REQUEST`
- `ENDTURN_REQUEST`
- `ENDGAME_REQUEST`

`server -> client`:
- `CONNECTION`
- `CREATENEWROOM_RESPONSE`
- `JOINROOM_RESPONSE`
- `LEAVEROOM_RESPONSE`
- `STARTNEWGAME_RESPONSE`
- `ENDTURN_RESPONSE`
- `ENDGAME_RESPONSE`
- `ERROR`

`DISCONNECTION` jest logowane po stronie serwera przy zamykaniu sesji.

### 5.3 Walidacja requestow

- `CREATENEWROOM_REQUEST`: wymagane `roomId`; pokoj nie moze istniec; klient nie moze byc juz w pokoju.
- `JOINROOM_REQUEST`: wymagane `roomId`; pokoj musi istniec; klient nie moze byc juz w pokoju.
- `LEAVEROOM_REQUEST`: wymagane `roomId`; klient musi byc w pokoju; pokoj musi istniec.
- `STARTNEWGAME_REQUEST`: wymagane `roomId` i `playerId`; klient musi nalezec do pokoju; pokoj nie moze miec aktywnej gry.
- `ACTION_REQUEST`: wymagane `playerId`; `gameId` musi istniec; `actionData` przyjmuje JSON.
- `ENDTURN_REQUEST`: wymagane `gameId`; `gameId` musi istniec.
- `ENDGAME_REQUEST`: wymagane `gameId`; `gameId` musi istniec.

### 5.4 Formaty JSON - requesty

#### CREATENEWROOM_REQUEST

```json
{
  "messageType": "CREATENEWROOM_REQUEST",
  "clientId": "58a84c5a-ca0e-4a8d-bf04-11ae1152bdf4",
  "roomId": "room-1",
  "playerName": "Anna"
}
```

#### JOINROOM_REQUEST

```json
{
  "messageType": "JOINROOM_REQUEST",
  "clientId": "58a84c5a-ca0e-4a8d-bf04-11ae1152bdf4",
  "roomId": "room-1",
  "playerName": "Bob"
}
```

#### LEAVEROOM_REQUEST

```json
{
  "messageType": "LEAVEROOM_REQUEST",
  "clientId": "58a84c5a-ca0e-4a8d-bf04-11ae1152bdf4",
  "roomId": "room-1",
  "playerName": "Bob"
}
```

#### STARTNEWGAME_REQUEST

```json
{
  "messageType": "STARTNEWGAME_REQUEST",
  "clientId": "58a84c5a-ca0e-4a8d-bf04-11ae1152bdf4",
  "roomId": "room-1",
  "playerId": "Anna",
  "playerName": "Anna",
  "scenario": "Moloch"
}
```

#### ACTION_REQUEST

```json
{
  "messageType": "ACTION_REQUEST",
  "clientId": "58a84c5a-ca0e-4a8d-bf04-11ae1152bdf4",
  "gameId": "8ef7dcb4-db11-4ddb-a8fc-2440391462bf",
  "playerId": "Anna",
  "actionData": {
    "action": "MOVE",
    "unitId": "u-12",
    "to": {
      "x": 3,
      "y": 5
    }
  }
}
```

#### ENDTURN_REQUEST

```json
{
  "messageType": "ENDTURN_REQUEST",
  "clientId": "58a84c5a-ca0e-4a8d-bf04-11ae1152bdf4",
  "gameId": "8ef7dcb4-db11-4ddb-a8fc-2440391462bf",
  "playerId": "Anna",
  "turnNumber": 1
}
```

#### ENDGAME_REQUEST

```json
{
  "messageType": "ENDGAME_REQUEST",
  "clientId": "58a84c5a-ca0e-4a8d-bf04-11ae1152bdf4",
  "gameId": "8ef7dcb4-db11-4ddb-a8fc-2440391462bf",
  "winnerId": "Anna",
  "reason": "Victory points"
}
```

### 5.5 Formaty JSON - odpowiedzi i zdarzenia

#### CONNECTION

```json
{
  "messageType": "CONNECTION",
  "timestamp": "2026-03-25T17:05:38.833822698",
  "clientId": "58a84c5a-ca0e-4a8d-bf04-11ae1152bdf4",
  "message": "Connected"
}
```

#### CREATENEWROOM_RESPONSE

```json
{
  "messageType": "CREATENEWROOM_RESPONSE",
  "timestamp": "2026-03-25T17:05:38.860000000",
  "clientId": "58a84c5a-ca0e-4a8d-bf04-11ae1152bdf4",
  "createdRoomId": "room-1",
  "serverStatus": "STARTED room=room-1 player=Anna"
}
```

#### JOINROOM_RESPONSE

```json
{
  "messageType": "JOINROOM_RESPONSE",
  "timestamp": "2026-03-25T17:05:38.861000000",
  "clientId": "58a84c5a-ca0e-4a8d-bf04-11ae1152bdf4",
  "serverStatus": "JOINED room=room-1 player=Bob"
}
```

#### LEAVEROOM_RESPONSE

```json
{
  "messageType": "LEAVEROOM_RESPONSE",
  "timestamp": "2026-03-25T17:05:38.862000000",
  "clientId": "58a84c5a-ca0e-4a8d-bf04-11ae1152bdf4",
  "serverStatus": "LEFT room=room-1 player=Bob"
}
```

#### STARTNEWGAME_RESPONSE

```json
{
  "messageType": "STARTNEWGAME_RESPONSE",
  "timestamp": "2026-03-25T17:05:38.865660438",
  "clientId": "58a84c5a-ca0e-4a8d-bf04-11ae1152bdf4",
  "roomId": "room-1",
  "playerId": "Anna",
  "createdGameId": "8ef7dcb4-db11-4ddb-a8fc-2440391462bf",
  "serverStatus": "STARTED room=room-1 game=8ef7dcb4-db11-4ddb-a8fc-2440391462bf player=Anna"
}
```

#### ENDTURN_RESPONSE

```json
{
  "messageType": "ENDTURN_RESPONSE",
  "timestamp": "2026-03-25T17:05:38.870845967",
  "clientId": "58a84c5a-ca0e-4a8d-bf04-11ae1152bdf4",
  "gameId": "8ef7dcb4-db11-4ddb-a8fc-2440391462bf",
  "accepted": true,
  "nextPlayerId": "Anna_next"
}
```

#### ENDGAME_RESPONSE

```json
{
  "messageType": "ENDGAME_RESPONSE",
  "timestamp": "2026-03-25T17:05:38.872774487",
  "clientId": "58a84c5a-ca0e-4a8d-bf04-11ae1152bdf4",
  "gameId": "8ef7dcb4-db11-4ddb-a8fc-2440391462bf",
  "ended": true,
  "summary": "Game ended. Winner=Anna, reason=Victory points"
}
```

#### ERROR

```json
{
  "messageType": "ERROR",
  "timestamp": "2026-03-25T17:05:39.000000000",
  "clientId": "58a84c5a-ca0e-4a8d-bf04-11ae1152bdf4",
  "error": "Unsupported messageType: FOO_REQUEST"
}
```

---

## 6. Klient Python

Implementacja klienta WebSocket znajduje sie tylko w `client/websocket_client.py`.

Parametry:
- `--server` (domyslnie: `ws://localhost:8080/ws/chat`)
- `-v`, `--verbose` (bardziej szczegolowe logowanie)

---

## 7. Testowanie

### Build Java

```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp
./gradlew test
```

### Build dokumentacji PDF (asciidoc2pdf)

Wymagane jest narzedzie `asciidoc2pdf` (np. z pakietu `asciidoc3`).

```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp
./gradlew docsPdf
```

Wynik:
- `build/docs/asciidoc/` - pliki tymczasowe `.adoc`
- `build/docs/pdf/` - pliki wynikowe `.pdf`

---

## 8. Logowanie

- konfiguracja: `src/main/resources/logback.xml`
- log serwera: `logs/websocket.log`
- logger aplikacji: `pl.staszic.neu`

Podglad logow:

```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp
tail -f logs/websocket.log
```

---

## 9. Troubleshooting

### Problem: `ModuleNotFoundError: websocket`

Zainstaluj zaleznosci w virtualenv:

```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp
.venv/bin/python -m pip install -r requirements.txt
```

### Problem: brak polaczenia z serwerem

1. uruchom backend (`./gradlew bootRun`)
2. sprawdz endpoint statystyk:

```bash
curl http://localhost:8080/api/websocket/stats
```

### Problem: zajety port 8080

Zmien port w konfiguracji Spring (`server.port`) lub zatrzymaj proces, ktory go uzywa.
