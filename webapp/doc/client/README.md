# Dokumentacja klienta WebSocket (Python)

## 1. Zakres

Ten dokument opisuje klienta z pliku `client/websocket_client.py` oraz kontrakt komunikatow WebSocket,
ktory klient wysyla i odbiera.

## 2. Klasy bazowe komunikatow

### 2.1 `WebSocketMessage`

Bazowa klasa kazdego komunikatu. Pola:
- `messageType` (`String`) - typ komunikatu, np. `JOINROOM_REQUEST`
- `timestamp` (`String`, ISO-8601) - czas utworzenia komunikatu
- `clientId` (`String`) - identyfikator klienta nadawany po polaczeniu

### 2.2 `GameScopedWebSocketMessage`

Rozszerza `WebSocketMessage` o pole:
- `gameId` (`String`) - identyfikator gry

## 3. Opis klas request/response

### 3.1 Request (`client -> server`)

#### `CreateNewRoomRequest` (`CREATENEWROOM_REQUEST`)
Pola:
- `roomId` (`String`)
- `playerName` (`String`)

#### `JoinRoomRequest` (`JOINROOM_REQUEST`)
Pola:
- `roomId` (`String`)
- `playerName` (`String`)

#### `LeaveRoomRequest` (`LEAVEROOM_REQUEST`)
Pola:
- `roomId` (`String`)
- `playerName` (`String`)

#### `GetRoomStatusRequest` (`GETROOMSTATUS_REQUEST`)
Pola:
- `roomId` (`String`)

#### `StartNewGameRequest` (`STARTNEWGAME_REQUEST`)
Pola:
- `roomId` (`String`)
- `playerId` (`String`)
- `playerName` (`String`)
- `scenario` (`String`)

#### `ActionRequest` (`ACTION_REQUEST`)
Dziedziczy po `GameScopedWebSocketMessage`.
Pola:
- `gameId` (`String`)
- `playerId` (`String`)
- `actionData` (`JSON`, dowolny obiekt)

#### `EndGameRequest` (`ENDGAME_REQUEST`)
Dziedziczy po `GameScopedWebSocketMessage`.
Pola:
- `gameId` (`String`)
- `winnerId` (`String`)
- `reason` (`String`)

### 3.2 Response i zdarzenia (`server -> client`)

#### `CreateNewRoomResponse` (`CREATENEWROOM_RESPONSE`)
Pola:
- `createdRoomId` (`String`)
- `serverStatus` (`String`)

#### `JoinRoomResponse` (`JOINROOM_RESPONSE`)
Pola:
- `serverStatus` (`String`)

#### `LeaveRoomResponse` (`LEAVEROOM_RESPONSE`)
Pola:
- `serverStatus` (`String`)

#### `GetRoomStatusResponse` (`GETROOMSTATUS_RESPONSE`)
Pola:
- `serverStatus` (`String`)
- `roomId` (`String`)
- `playersInRoom` (`Set<String>`)
- `gameId` (`String`, opcjonalne)

#### `StartNewGameResponse` (`STARTNEWGAME_RESPONSE`)
Pola:
- `createdGameId` (`String`)
- `roomId` (`String`)
- `playerId` (`String`)
- `serverStatus` (`String`)

#### `EndGameResponse` (`ENDGAME_RESPONSE`)
Dziedziczy po `GameScopedWebSocketMessage`.
Pola:
- `gameId` (`String`)
- `ended` (`boolean`)
- `summary` (`String`)

#### `CONNECTION`
Zdarzenie inicjalne po polaczeniu.
Pola:
- `messageType`
- `timestamp`
- `clientId`
- `message`

#### `ERROR`
Zdarzenie bledu walidacji/protokolu.
Pola:
- `messageType`
- `timestamp`
- `clientId`
- `error`

## 4. Sekwencje wywolan (mozliwe flow)

### 4.1 Nawiazywanie polaczenia
1. Klient laczy sie z `ws://localhost:8080/ws/chat`.
2. Serwer odsyla `CONNECTION` z `clientId`.
3. Klient zapisuje `clientId` i dolacza je automatycznie do kolejnych requestow.

### 4.2 Flow tworzenia pokoju i startu gry
1. `CREATENEWROOM_REQUEST`
2. `CREATENEWROOM_RESPONSE`
3. (drugi klient) `JOINROOM_REQUEST`
4. (drugi klient) `JOINROOM_RESPONSE`
5. `STARTNEWGAME_REQUEST`
6. `STARTNEWGAME_RESPONSE` (z `createdGameId`)
7. Nastepnie mozliwe `ACTION_REQUEST`, `ENDGAME_REQUEST`

### 4.3 Flow dolaczenia do istniejacego pokoju
1. `JOINROOM_REQUEST`
2. `JOINROOM_RESPONSE`
3. Opcjonalnie `GETROOMSTATUS_REQUEST`
4. `GETROOMSTATUS_RESPONSE`

### 4.4 Flow opuszczenia pokoju
1. `LEAVEROOM_REQUEST`
2. `LEAVEROOM_RESPONSE`

### 4.5 Flow tury i zakonczenia gry
1. `ACTION_REQUEST` (powtarzalne)
2. `ENDGAME_REQUEST`
3. `ENDGAME_RESPONSE`

### 4.6 Flow bledow
- Dla niepoprawnego `messageType` lub niepelnych danych serwer odsyla `ERROR`.

## 5. Przykladowe JSON dla kazdej klasy

### 5.1 `CreateNewRoomRequest`
```json
{
  "messageType": "CREATENEWROOM_REQUEST",
  "clientId": "58a84c5a-ca0e-4a8d-bf04-11ae1152bdf4",
  "roomId": "room-1",
  "playerName": "Anna"
}
```

### 5.2 `CreateNewRoomResponse`
```json
{
  "messageType": "CREATENEWROOM_RESPONSE",
  "timestamp": "2026-03-29T11:00:00",
  "clientId": "58a84c5a-ca0e-4a8d-bf04-11ae1152bdf4",
  "createdRoomId": "room-1",
  "serverStatus": "STARTED room=room-1 player=Anna"
}
```

### 5.3 `JoinRoomRequest`
```json
{
  "messageType": "JOINROOM_REQUEST",
  "clientId": "b8f25c47-8c48-4e58-b1ea-d38e2e6e8d48",
  "roomId": "room-1",
  "playerName": "Bob"
}
```

### 5.4 `JoinRoomResponse`
```json
{
  "messageType": "JOINROOM_RESPONSE",
  "timestamp": "2026-03-29T11:00:01",
  "clientId": "b8f25c47-8c48-4e58-b1ea-d38e2e6e8d48",
  "serverStatus": "JOINED room=room-1 player=Bob"
}
```

### 5.5 `LeaveRoomRequest`
```json
{
  "messageType": "LEAVEROOM_REQUEST",
  "clientId": "b8f25c47-8c48-4e58-b1ea-d38e2e6e8d48",
  "roomId": "room-1",
  "playerName": "Bob"
}
```

### 5.6 `LeaveRoomResponse`
```json
{
  "messageType": "LEAVEROOM_RESPONSE",
  "timestamp": "2026-03-29T11:00:02",
  "clientId": "b8f25c47-8c48-4e58-b1ea-d38e2e6e8d48",
  "serverStatus": "LEFT room=room-1 player=Bob"
}
```

### 5.7 `GetRoomStatusRequest`
```json
{
  "messageType": "GETROOMSTATUS_REQUEST",
  "clientId": "58a84c5a-ca0e-4a8d-bf04-11ae1152bdf4",
  "roomId": "room-1"
}
```

### 5.8 `GetRoomStatusResponse`
```json
{
  "messageType": "GETROOMSTATUS_RESPONSE",
  "timestamp": "2026-03-29T11:00:03",
  "clientId": "58a84c5a-ca0e-4a8d-bf04-11ae1152bdf4",
  "roomId": "room-1",
  "playersInRoom": [
    "58a84c5a-ca0e-4a8d-bf04-11ae1152bdf4",
    "b8f25c47-8c48-4e58-b1ea-d38e2e6e8d48"
  ],
  "gameId": null,
  "serverStatus": "STATUS for room=room-1"
}
```

### 5.9 `StartNewGameRequest`
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

### 5.10 `StartNewGameResponse`
```json
{
  "messageType": "STARTNEWGAME_RESPONSE",
  "timestamp": "2026-03-29T11:00:04",
  "clientId": "58a84c5a-ca0e-4a8d-bf04-11ae1152bdf4",
  "roomId": "room-1",
  "playerId": "Anna",
  "createdGameId": "8ef7dcb4-db11-4ddb-a8fc-2440391462bf",
  "serverStatus": "STARTED room=room-1 game=8ef7dcb4-db11-4ddb-a8fc-2440391462bf player=Anna"
}
```

### 5.11 `ActionRequest`
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

### 5.12 `EndGameRequest`
```json
{
  "messageType": "ENDGAME_REQUEST",
  "clientId": "58a84c5a-ca0e-4a8d-bf04-11ae1152bdf4",
  "gameId": "8ef7dcb4-db11-4ddb-a8fc-2440391462bf",
  "winnerId": "Anna",
  "reason": "Victory points"
}
```

### 5.13 `EndGameResponse`
```json
{
  "messageType": "ENDGAME_RESPONSE",
  "timestamp": "2026-03-29T11:00:06",
  "clientId": "58a84c5a-ca0e-4a8d-bf04-11ae1152bdf4",
  "gameId": "8ef7dcb4-db11-4ddb-a8fc-2440391462bf",
  "ended": true,
  "summary": "Game ended. Winner=Anna, reason=Victory points"
}
```

### 5.14 `CONNECTION`
```json
{
  "messageType": "CONNECTION",
  "timestamp": "2026-03-29T11:00:00",
  "clientId": "58a84c5a-ca0e-4a8d-bf04-11ae1152bdf4",
  "message": "Connected"
}
```

### 5.15 `ERROR`
```json
{
  "messageType": "ERROR",
  "timestamp": "2026-03-29T11:00:07",
  "clientId": "58a84c5a-ca0e-4a8d-bf04-11ae1152bdf4",
  "error": "Unsupported messageType: FOO_REQUEST"
}
```

## 6. Generowanie PDF z dokumentacji

W projekcie dostepne jest zadanie Gradle `docsPdf`, ktore:
1. konwertuje pliki `*.md` z katalogu `doc/` do `*.adoc`,
2. generuje pliki PDF przy uzyciu `asciidoc2pdf`.

Uruchomienie:

```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp
./gradlew docsPdf
```

Wynik:
- pliki `.adoc`: `build/docs/asciidoc/`
- pliki `.pdf`: `build/docs/pdf/`

