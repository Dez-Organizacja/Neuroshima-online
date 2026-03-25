# WebSocket Application - Neuroshima

> Aplikacja komunikacji czasu rzeczywistego z serwerem WebSocket w Javie i klientem w Pythonie.

[![Status](https://img.shields.io/badge/status-Production-brightgreen)]()
[![Java](https://img.shields.io/badge/Java-17+-blue)]()
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.0.0-green)]()
[![Python](https://img.shields.io/badge/Python-3.7+-blue)]()

## 📋 Spis treści

- [Szybki Start](#szybki-start)
- [Funkcjonalności](#funcjonalności)
- [Instalacja](#instalacja)
- [Uruchamianie](#uruchamianie)
- [Testowanie](#testowanie)
- [Dokumentacja](#dokumentacja)

---

## 🚀 Szybki Start

### Krok 1: Uruchom serwer

```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp
./gradlew bootRun
```

Czekaj aż zobaczysz:
```
Started Main in X.XXX seconds
Tomcat started on port(s): 8080
```

### Krok 2: Uruchom klienta

W nowym terminalu:
```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp/client
python websocket_client.py
```

### Krok 3: Testuj!

```
CONNECTED {...}
RESPONSE {"messageType":"STARTNEWGAME_RESPONSE", ...}
RESPONSE {"messageType":"ENDTURN_RESPONSE", ...}
RESPONSE {"messageType":"ENDGAME_RESPONSE", ...}
```

---

## ✨ Funkcjonalności

### Serwer
- ✅ WebSocket na `ws://localhost:8080/ws/chat`
- ✅ Obsługa wielu klientów
- ✅ Echo wiadomości
- ✅ Broadcast do wszystkich
- ✅ Unikalne ID (UUID) dla każdego klienta
- ✅ Logowanie do pliku i konsoli
- ✅ REST API dla statystyk

### Klient
- ✅ Klient Python dla protokołu gry
- ✅ Przykład klas komunikatów (`client/game_messages_example.py`)
- ✅ Parametry uruchomienia (`--server`, `--player`, `--scenario`, `--turn`, `--reason`)

### Komunikacja
- ✅ Wiadomości w JSON
- ✅ Typy: `STARTNEWGAME`, `ENDTURN`, `ENDGAME` (request/response)
- ✅ Timestamp (ISO-8601)
- ✅ Client ID (UUID)
- ✅ `gameId` wymagane dla `ENDTURN` i `ENDGAME`

---

## 📦 Instalacja

### Wymagania
- Java 17+
- Python 3.7+
- Gradle (jest w projekcie)

### Setup

```bash
# 1. Clone / Navigate
cd /home/dawid/cpp/projekty/Neuroshima/webapp

# 2. Zainstaluj Python dependencies
pip install -r requirements.txt
# LUB
pip install websocket-client
```

---

## ▶️ Uruchamianie

### Serwer WebSocket

```bash
# Metoda 1: Gradle
./gradlew bootRun

# Metoda 2: JAR
./gradlew bootJar
java -jar build/libs/webapp-1.0-SNAPSHOT.jar
```

Server nasłuchuje na:
- **WebSocket**: `ws://localhost:8080/ws/chat`
- **REST**: `http://localhost:8080/api/websocket/stats`

### Klient WebSocket

```bash
cd client

# Domyślnie
python websocket_client.py

# Z parametrami
python websocket_client.py --server ws://192.168.1.100:8080/ws/chat --player "Bot-1"

# Przykład klas request/response
python game_messages_example.py
```

Parametry:
- `--server` - URL serwera (default: ws://localhost:8080/ws/chat)
- `--player` - Nazwa gracza (default: Anna)
- `--scenario` - Scenariusz (default: Moloch)
- `--turn` - Numer tury (default: 1)
- `--reason` - Powod zakonczenia gry

---

## 🧪 Testowanie

### Testy automatyczne

```bash
cd client
python test.py
```

### Test manualny

```bash
# Terminal 1: Serwer
./gradlew bootRun

# Terminal 2: Klient Python
cd client && python websocket_client.py --player "Klient-1"

# Terminal 4: Sprawdź statystyki
curl http://localhost:8080/api/websocket/stats
# {"activeConnections": 2, "status": "OK"}
```

---

## 📋 Komunikaty JSON

### Połączenie
```json
{
  "messageType": "CONNECTION",
  "timestamp": "2026-03-17T14:25:30.123456",
  "clientId": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Connected"
}
```

### STARTNEWGAME_REQUEST
```json
{
  "messageType": "STARTNEWGAME_REQUEST",
  "timestamp": "2026-03-17T14:25:35.654321",
  "clientId": "550e8400-e29b-41d4-a716-446655440000",
  "playerName": "Anna",
  "scenario": "Moloch"
}
```

### ENDTURN_REQUEST
```json
{
  "messageType": "ENDTURN_REQUEST",
  "timestamp": "2026-03-17T14:25:35.789012",
  "clientId": "550e8400-e29b-41d4-a716-446655440000",
  "gameId": "5d4a3a11-e294-461c-a763-2588fa854152",
  "playerId": "Anna",
  "turnNumber": 1
}
```

---

## 📝 Logowanie

### Serwer

Plik: `logs/websocket.log`

Konfiguracja: `src/main/resources/logback.xml`

```
2026-03-17 14:25:30.123 [main] INFO pl.staszic.neu.Main - Starting Main
2026-03-17 14:25:31.234 [thread-1] INFO pl.staszic.neu.WebSocketHandler - New client connected
```

### Klient

Plik: `client/client.log`

```
2026-03-17 14:25:30 [INFO] WebSocket Client uruchomiony
2026-03-17 14:25:31 [INFO] Serwer: ws://localhost:8080/ws/chat
2026-03-17 14:25:31 [INFO] ✅ Połączono! ID klienta: 550e8400...
```

---

## 📂 Struktura projektu

```
webapp/
├── QUICKSTART.md                      ← 5-minutowy przewodnik
├── README.md                          ← Ten plik
├── IMPLEMENTATION_SUMMARY.md          ← Podsumowanie pracy
├── requirements.txt                   ← Python dependencies
├── build.gradle.kts                   ← Gradle config
├── src/main/
│   ├── java/pl/staszic/neu/
│   │   ├── Main.java                  ← Entry point
│   │   ├── WebSocketConfig.java       ← WebSocket config
│   │   ├── WebSocketHandler.java      ← Handler protokolu gry
│   │   ├── WebSocketController.java   ← REST endpoint
│   │   ├── MathService.java
│   │   └── messages/
│   │       ├── WebSocketMessage.java
│   │       ├── StartNewGameRequest.java
│   │       ├── StartNewGameResponse.java
│   │       ├── EndTurnRequest.java
│   │       ├── EndTurnResponse.java
│   │       ├── EndGameRequest.java
│   │       └── EndGameResponse.java
│   └── resources/
│       ├── logback.xml                ← Logging config
│       └── static/                    ← (pusty - klient w Pythonie)
├── client/
│   ├── websocket_client.py            ← Main client
│   ├── game_messages_example.py       ← Example request/response classes
│   ├── test.py                        ← Protocol smoke test
│   ├── test.json
│   └── client.log                     ← Generated
├── doc/
│   ├── INDEX.md                       ← Start tutaj!
│   ├── README.md                      ← Full docs
│   └── prompt-websocket.txt           ← Wymagania
└── logs/
    └── websocket.log                  ← Generated
```

---

## 🎯 Wymagania

Wszystkie wymagania z `doc/prompt-websocket.txt` zostały spełnione:

- ✅ Serwer WebSocket
- ✅ Klient WebSocket w Pythonie
- ✅ STARTNEWGAME / ENDTURN / ENDGAME (Request i Response)
- ✅ Dziedziczenie komunikatów i `gameId` poza STARTNEWGAME
- ✅ Logowanie
- ✅ Format JSON
- ✅ Komentarze w kodzie
- ✅ Dokumentacja

---

## 🔧 Zaawansowane

### Zmiana portu

Edytuj `src/main/resources/application.properties`:
```properties
server.port=8081
```

### Zmiana ścieżki WebSocket

Edytuj `WebSocketConfig.java`:
```java
registry.addHandler(new WebSocketHandler(), "/ws/custom");
```

### Zmiana poziomu logowania

Edytuj `logback.xml`:
```xml
<root level="DEBUG">  <!-- zmień z INFO na DEBUG -->
```

---

## 🐛 Rozwiązywanie problemów

| Problem | Rozwiązanie |
|---------|------------|
| Port 8080 zajęty | Zmień port lub zabij proces: `lsof -i :8080` |
| ModuleNotFoundError: websocket | `pip install websocket-client` |
| Connection refused | Sprawdź czy serwer działa |
| Timeout | Serwer nie odpowiada w ciągu 5 sekund |

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
- `websocket_client.py` - Klient sekwencyjny dla START/ENDTURN/ENDGAME
- `test.py` - Test smoke nowego protokołu

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
  - Komunikaty: baza + klasy STARTNEWGAME/ENDTURN/ENDGAME
  - Logback.xml: 46 linii

Python:
  - websocket_client.py: klient CLI dla protokolu gry
  - test.py: prosty test end-to-end

Dokumentacja:
  - README.md
  - QUICKSTART.md
  - IMPLEMENTATION_SUMMARY.md
```

---

## ✅ Status

- ✅ Kod skompilowany bez błędów
- ✅ Serwer startuje
- ✅ Klient działa
- ✅ Testy przechodzą
- ✅ Dokumentacja kompletna
- ✅ Gotowe do produkcji

---

## 📄 Licencja

Część projektu Neuroshima - 2026

---

## 🎉 Uwagi

> "Całą aplikację można uruchomić w 5 minut bez żadnych problemów." - Instrukcja QUICKSTART

**Zacznij tutaj:** [QUICKSTART.md](QUICKSTART.md)

```bash
# W jednej linijce:
./gradlew bootRun & sleep 2 && cd client && python websocket_client.py --player "Bot-1"
```

---

**Happy WebSocketing! 🚀**

