# Dokumentacja - Index

Punkt wejscia do dokumentacji projektu WebSocket Neuroshima.

## Gdzie zaczac

- szybki start: `QUICKSTART.md`
- pelny opis protokolu: `doc/README.md`
- dokumentacja klienta Python: `doc/client/README.md`
- przeglad zmian: `IMPLEMENTATION_SUMMARY.md`
- glowny opis repo: `README.md`

## Aktualny stan projektu

- backend: Java/Spring Boot (`pl.staszic.neu`)
- websocket: `ws://localhost:8080/ws/chat`
- klient: implementacja w `client/websocket_client.py`

Typy requestow (`client -> server`):
1. `CREATENEWROOM_REQUEST`
2. `JOINROOM_REQUEST`
3. `LEAVEROOM_REQUEST`
4. `STARTNEWGAME_REQUEST`
5. `ACTION_REQUEST` (`actionData` przyjmuje JSON)
6. `ENDGAME_REQUEST`

Typy odpowiedzi/zdarzen (`server -> client`):
1. `CONNECTION`
2. `CREATENEWROOM_RESPONSE`
3. `JOINROOM_RESPONSE`
4. `LEAVEROOM_RESPONSE`
5. `STARTNEWGAME_RESPONSE`
6. `ENDGAME_RESPONSE`
7. `ERROR`

Uwaga: `DISCONNECTION` jest generowane przy zamknieciu sesji i logowane po stronie serwera.

## Najwazniejsze pliki

```text
webapp/
├── QUICKSTART.md
├── README.md
├── IMPLEMENTATION_SUMMARY.md
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
│   └── websocket_client.py
└── doc/
    ├── INDEX.md
    ├── README.md
    └── prompty/
```

## Szybkie komendy

```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp
./gradlew bootRun
```

```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp/client
../.venv/bin/python websocket_client.py --server ws://localhost:8080/ws/chat
```

Najczestsze problemy:

- `ModuleNotFoundError: websocket` -> `../.venv/bin/python -m pip install -r ../requirements.txt`
- `Timeout` -> serwer jest niedostepny, sprawdz logi w `logs/websocket.log`

Szczegoly: `doc/README.md`

Dokumentacja klienta: `doc/client/README.md`

