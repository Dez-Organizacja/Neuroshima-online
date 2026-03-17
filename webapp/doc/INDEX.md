# 📚 WebSocket Application - Dokumentacja

Witaj w aplikacji WebSocket Neuroshima! Poniżej znajdziesz wszystkie potrzebne informacje.

## 🚀 Szybki Start (5 minut)

Chcesz szybko uruchomić aplikację?

→ **Przeczytaj: [QUICKSTART.md](../QUICKSTART.md)**

```bash
# Terminal 1 - Serwer
./gradlew bootRun

# Terminal 2 - Klient
cd client && python websocket_client.py
```

---

## 📖 Pełna Dokumentacja

Potrzebujesz szczegółowych informacji?

→ **Przeczytaj: [README.md](README.md)**

Zawiera:
- ✅ Architektura systemu
- ✅ Instalacja i konfiguracja
- ✅ Format komunikatów JSON
- ✅ Testowanie aplikacji
- ✅ Konfiguracja logowania
- ✅ Rozwiązywanie problemów

---

## 📋 Podsumowanie Implementacji

Chcesz zobaczyć co zostało zrobione?

→ **Przeczytaj: [../IMPLEMENTATION_SUMMARY.md](../IMPLEMENTATION_SUMMARY.md)**

Zawiera:
- ✅ Wykaz wszystkich zmienionych plików
- ✅ Spełnione wymagania
- ✅ Struktura projektu
- ✅ Wyniki testów

---

## 🎯 Wymagania Oryginalne

Przejrzyj oryginalne polecenie:

→ **[prompt-websocket.txt](prompty/prompt-websocket.txt)**

---

## 📂 Struktura Plików

```
webapp/
├── 📄 QUICKSTART.md              ← Szybki start (5 min)
├── 📄 IMPLEMENTATION_SUMMARY.md   ← Co zostało zrobione
├── 📄 README.md                  ← Full documentation (QUICKSTART.md)
├── 📄 requirements.txt            ← Python dependencies
├── src/main/
│   ├── java/org/example/
│   │   ├── WebSocketConfig.java      ← WebSocket config
│   │   ├── WebSocketHandler.java     ← Main handler (290 lines)
│   │   ├── WebSocketMessage.java     ← JSON DTO
│   │   └── ... (inne klasy)
│   └── resources/
│       ├── logback.xml               ← Logging config
│       └── static/                   ← (pusty, HTML usunięty)
├── client/
│   ├── websocket_client.py           ← Main client (444 lines)
│   ├── test.py                       ← Tests (400+ lines)
│   └── client.log                    ← Generated logs
└── doc/
    ├── INDEX.md                      ← To jest ten plik
    ├── README.md                     ← Full documentation
    └── prompt-websocket.txt          ← Original requirements
```

---

## ✨ Funkcjonalności

### Serwer WebSocket
- ✅ Nasłuchuje na `ws://localhost:8080/ws/chat`
- ✅ Obsługuje wiele klientów jednocześnie
- ✅ Echo wiadomości
- ✅ Broadcast do wszystkich klientów
- ✅ Unikalny UUID dla każdego klienta
- ✅ Pełne logowanie

### Klient Python
- ✅ Interaktywny tryb
- ✅ Obsługa komend (`/status`, `/exit`, `/help`)
- ✅ Logowanie do pliku i konsoli
- ✅ Obsługa błędów
- ✅ Parametry wiersza poleceń

### Komunikaty JSON
- ✅ Type: connection, message, echo, disconnection
- ✅ Timestamp: ISO-8601
- ✅ ClientId: UUID
- ✅ Message: Treść wiadomości

### Logowanie
- ✅ Serwer: `logs/websocket.log` (SLF4J + Logback)
- ✅ Klient: `client/client.log` (Python logging)
- ✅ Archiwizacja i rotacja
- ✅ Różne level'e (DEBUG, INFO)

---

## 🔧 Podstawowe Komendy

### Uruchomienie serwera
```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp
./gradlew bootRun
```

### Uruchomienie klienta
```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp/client
python websocket_client.py
```

### Uruchomienie testów
```bash
python test.py              # Wszystkie testy
python test.py connection   # Konkretny test
python test.py echo
python test.py broadcast
```

### Sprawdzenie logów
```bash
# Serwer
tail -f logs/websocket.log

# Klient
tail -f client/client.log
```

### Statystyki
```bash
curl http://localhost:8080/api/websocket/stats
```

---

## 🧪 Testowanie

### Test 1: Połączenie
```bash
python websocket_client.py
# Powinieneś zobaczyć: ✅ Połączono!
```

### Test 2: Echo
```
> Cześć serwer!
[14:25:35] 📤 Ty: Cześć serwer!
[14:25:35] 📥 Echo: Cześć serwer!
```

### Test 3: Status
```
> /status
[14:25:40] ℹ️ Status: Połączono ✅ | ID: 550e8400...
```

### Test 4: Wiele klientów
```bash
# Terminal 1
python websocket_client.py --name "Klient-1"

# Terminal 2
python websocket_client.py --name "Klient-2"

# Terminal 3
curl http://localhost:8080/api/websocket/stats
# Result: {"activeConnections": 2, "status": "OK"}
```

---

## 📝 Formaty Komunikatów

### Połączenie (server → client)
```json
{
  "type": "connection",
  "timestamp": "2026-03-17T14:25:30.123456",
  "clientId": "550e8400-e29b-41d4-a716-446655440000",
  "message": null
}
```

### Wiadomość (client → server)
```json
{
  "type": "message",
  "timestamp": "2026-03-17T14:25:35.654321",
  "clientId": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Cześć serwer!"
}
```

### Echo (server → client)
```json
{
  "type": "echo",
  "timestamp": "2026-03-17T14:25:35.789012",
  "clientId": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Cześć serwer!"
}
```

---

## ⚙️ Parametry Klienta

```bash
python websocket_client.py [opcje]

Opcje:
  --server WS_URL      Server URL (default: ws://localhost:8080/ws/chat)
  --name NAME          Client name (default: PythonClient)
  --log FILE           Log file (default: client.log)
```

### Przykłady:
```bash
# Domyślne ustawienia
python websocket_client.py

# Zmień serwer
python websocket_client.py --server ws://192.168.1.100:8080/ws/chat

# Zmień nazwę klienta
python websocket_client.py --name "Bot-1"

# Wszystkie opcje
python websocket_client.py --server ws://localhost:8080/ws/chat --name "Test" --log test.log
```

---

## 🐛 Rozwiązywanie Problemów

| Problem | Rozwiązanie |
|---------|-------------|
| "Connection refused" | Sprawdź czy serwer działa: `curl http://localhost:8080/api/websocket/stats` |
| "Port 8080 już zajęty" | Zmień port w `application.properties` lub zabij proces |
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

