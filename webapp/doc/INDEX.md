# Dokumentacja - Index

Punkt wejścia do aktualnej dokumentacji projektu WebSocket Neuroshima.

## Gdzie zacząć

- szybki start: `QUICKSTART.md`
- pełny opis: `doc/README.md`
- przegląd zmian: `IMPLEMENTATION_SUMMARY.md`
- główny opis repo: `README.md`

## Aktualny stan projektu

- backend: Java/Spring Boot (`pl.staszic.neu`)
- websocket: `ws://localhost:8080/ws/chat`
- protokół: `STARTNEWGAME`, `ENDTURN`, `ENDGAME` (request/response)
- klient: wyłącznie Python (`client/websocket_client.py`)

## Najważniejsze pliki

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
│       ├── StartNewGameRequest.java
│       ├── StartNewGameResponse.java
│       ├── EndTurnRequest.java
│       ├── EndTurnResponse.java
│       ├── EndGameRequest.java
│       └── EndGameResponse.java
├── client/
│   ├── websocket_client.py
│   ├── game_messages_example.py
│   └── test.py
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
../.venv/bin/python websocket_client.py
```

```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp/client
../.venv/bin/python test.py
```
| "ModuleNotFoundError: websocket" | `pip install websocket-client` |
| "Timeout" | Serwer jest niedostępny, sprawdź logi |

Szczegóły: **[README.md](README.md#rozwiązywanie-problemów)**

---

## 📚 Dodatkowe Zasoby

- [QUICKSTART.md](../QUICKSTART.md) - 5-minutowy przewodnik
- [README.md](README.md) - Pełna dokumentacja
- [../IMPLEMENTATION_SUMMARY.md](../IMPLEMENTATION_SUMMARY.md) - Podsumowanie pracy
- [prompt-websocket.txt](prompty/prompt-websocket.txt) - Oryginalne wymagania

---

## 🎉 Gotowy do użytku!

```
✅ Serwer WebSocket - Java/Spring Boot
✅ Klient WebSocket - Python
✅ Komunikaty JSON
✅ Logowanie
✅ Testowanie
✅ Dokumentacja
```

**Zacznij od:** [QUICKSTART.md](../QUICKSTART.md)

---

## 📞 Podsumowanie

Aplikacja WebSocket jest w pełni funkcjonalna i gotowa do użytku.

Jeśli masz pytania, sprawdź:
1. Logi serwera: `logs/websocket.log`
2. Logi klienta: `client/client.log`
3. Dokumentację: [README.md](README.md)

**Happy WebSocketing! 🚀**

