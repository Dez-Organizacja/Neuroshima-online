# Dokumentacja Aplikacji WebSocket - Neuroshima

## Spis treści
1. [Przegląd](#przegląd)
2. [Architektura](#architektura)
3. [Wymagania](#wymagania)
4. [Instalacja i konfiguracja](#instalacja-i-konfiguracja)
5. [Uruchamianie serwera](#uruchamianie-serwera)
6. [Uruchamianie klienta](#uruchamianie-klienta)
7. [Format komunikatów JSON](#format-komunikatów-json)
8. [Testowanie](#testowanie)
9. [Logowanie](#logowanie)
10. [Rozwiązywanie problemów](#rozwiązywanie-problemów)

---

## Przegląd

Aplikacja WebSocket to system komunikacji czasu rzeczywistego oparty na Spring Boot. Składa się z:
- **Serwera WebSocket** napisanego w Javie z Spring Boot
- **Klienta WebSocket** napisanego w Pythonie
- **Systemu logowania** z użyciem SLF4J i Logback

### Cechy
- ✅ Obsługa wielu klientów jednocześnie
- ✅ Echo wiadomości
- ✅ Komunikaty w formacie JSON
- ✅ Logowanie do pliku i konsoli
- ✅ Bezpieczne zamykanie połączeń
- ✅ Tryb interaktywny dla klienta

---

## Architektura

```
┌─────────────────────────────────────┐
│      Spring Boot Server             │
│  ┌──────────────────────────────┐  │
│  │  WebSocketConfig             │  │
│  │  - Rejestracja handlera      │  │
│  │  - Konfiguracja ścieżki      │  │
│  └──────────────────────────────┘  │
│               │                      │
│  ┌──────────────────────────────┐  │
│  │  WebSocketHandler            │  │
│  │  - Obsługa połączeń          │  │
│  │  - Przetwarzanie wiadomości  │  │
│  │  - Broadcast do klientów     │  │
│  └──────────────────────────────┘  │
│               │                      │
│  ┌──────────────────────────────┐  │
│  │  WebSocketMessage (DTO)      │  │
│  │  - type, timestamp           │  │
│  │  - clientId, message         │  │
│  └──────────────────────────────┘  │
│               │                      │
│  ┌──────────────────────────────┐  │
│  │  Logback (logging)           │  │
│  │  - logs/websocket.log        │  │
│  └──────────────────────────────┘  │
└─────────────────────────────────────┘
           WebSocket (ws://)
              │
              ├─────────────────┐
              │                 │
        ┌─────────────┐   ┌──────────────┐
        │ Python      │   │ Python       │
        │ Client 1    │   │ Client 2     │
        └─────────────┘   └──────────────┘
```

---

## Wymagania

### Serwer
- Java 17 lub nowsze
- Gradle (do budowania)
- Spring Boot 3.0.0

### Klient
- Python 3.7 lub nowsze
- Biblioteka `websocket-client`

---

## Instalacja i konfiguracja

### 1. Przygotowanie serwera

#### a) Zainstaluj wymagane pakiety
```bash
# Gradle jest już dostępny w projekcie (./gradlew)
# Zweryfikuj zainstalowanie Java
java -version
```

#### b) Struktura projektu Java
```
src/main/java/org/example/
├── Main.java                    # Punkt wejścia
├── WebSocketConfig.java         # Konfiguracja WebSocket
├── WebSocketHandler.java        # Handler obsługujący zdarzenia
├── WebSocketMessage.java        # DTO dla komunikatów JSON
├── WebSocketController.java     # REST endpoint dla statystyk
└── MathService.java             # Dodatkowa usługa

src/main/resources/
├── logback.xml                  # Konfiguracja logowania
└── static/
    └── (index.html został usunięty - używamy klienta w Pythonie)
```

#### c) Konfiguracja logowania (logback.xml)
Logowanie jest już skonfigurowane do:
- **Konsoli**: INFO level
- **Pliku**: `logs/websocket.log` (DEBUG level)
- **Archiwizacji**: Codziennie lub przy 10MB

```xml
<!-- Format logów -->
%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n
```

### 2. Przygotowanie klienta

#### a) Zainstaluj biblioteki Pythona
```bash
cd client
pip install websocket-client
```

#### b) Struktura klienta
```
client/
├── websocket_client.py          # Główny klient (zaktualizowany)
├── websocket_client.py          # Alternatywny skrypt
├── test.json                    # Dane testowe
└── client.log                   # Logi klienta (generowany)
```

---

## Uruchamianie serwera

### Metoda 1: Zabudowanie i uruchomienie

```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp

# Zabuduj projekt
./gradlew build

# Uruchom serwer
./gradlew bootRun
```

### Metoda 2: Uruchomienie z JAR

```bash
./gradlew bootJar
java -jar build/libs/webapp-1.0-SNAPSHOT.jar
```

### Potwierdzenie uruchomienia

Serwer powinien wyświetlić:
```
Started Main in X.XXX seconds (JVM running for Y.YYY)
```

Serwer nasłuchuje na:
- **WebSocket URL**: `ws://localhost:8080/ws/chat`
- **REST Endpoint**: `http://localhost:8080/api/websocket/stats`

---

## Uruchamianie klienta

### Uruchomienie podstawowe

```bash
cd client
python websocket_client.py
```

### Parametry uruchomienia

```bash
# Połączenie z domyślnym serwerem
python websocket_client.py

# Zmiana serwera
python websocket_client.py --server ws://192.168.1.100:8080/ws/chat

# Zmiana nazwy klienta
python websocket_client.py --name "MojKlient"

# Zmiana pliku logów
python websocket_client.py --log moje_logi.log

# Kombinacja wszystkich opcji
python websocket_client.py \
    --server ws://localhost:8080/ws/chat \
    --name "Bot-1" \
    --log bot1.log
```

### Interfejs klienta

Po uruchomieniu zobaczysz:
```
[14:25:30] ⚙️ Połączono jako: PythonClient
[14:25:30] ⚙️ Dostępne komendy: /status, /exit, lub wpisz wiadomość
> 
```

### Komendy dostępne w kliencie

| Komenda | Opis |
|---------|------|
| `/status` | Wyświetla status połączenia i ID klienta |
| `/exit` | Rozłącza się z serwerem i kończy aplikację |
| `/help` | Wyświetla pomoc |
| `[tekst]` | Wysyła wiadomość do serwera (np. `Cześć`) |

---

## Format komunikatów JSON

### 1. Wiadomość połączenia (server → client)
Wysyłana automatycznie po nawiązaniu połączenia:

```json
{
  "type": "connection",
  "timestamp": "2026-03-17T14:25:30.123456",
  "clientId": "550e8400-e29b-41d4-a716-446655440000",
  "message": null
}
```

### 2. Wiadomość tekstu (client → server)
Wysyłana przez klienta:

```json
{
  "type": "message",
  "timestamp": "2026-03-17T14:25:35.654321",
  "clientId": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Cześć serwer!"
}
```

### 3. Wiadomość Echo (server → client)
Server odsyła wiadomość z typem `echo`:

```json
{
  "type": "echo",
  "timestamp": "2026-03-17T14:25:35.789012",
  "clientId": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Cześć serwer!"
}
```

### 4. Wiadomość rozłączenia (server → client)
Wysyłana gdy klient się rozłącza:

```json
{
  "type": "disconnection",
  "timestamp": "2026-03-17T14:25:40.345678",
  "clientId": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Client disconnected with status: 1000"
}
```

### Pola JSON

| Pole | Typ | Wymagane | Opis |
|------|-----|----------|------|
| `type` | String | ✓ | Typ komunikatu: `connection`, `message`, `echo`, `disconnection` |
| `timestamp` | String (ISO-8601) | ✓ | Czas wysłania w formacie `YYYY-MM-DDTHH:MM:SS.ffffff` |
| `clientId` | String (UUID) | ✓ | Unikalny identyfikator klienta |
| `message` | String | ✗ | Treść wiadomości (opcjonalne, zależy od typu) |

---

## Testowanie

### Test 1: Połączenie i Echo

#### Krok 1: Uruchom serwer
```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp
./gradlew bootRun
```

#### Krok 2: Uruchom klienta w nowym terminalu
```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp/client
python websocket_client.py
```

#### Oczekiwany wynik
```
[14:25:30] ⚙️ Połączono jako: PythonClient
[14:25:30] ⚙️ Dostępne komendy: /status, /exit, lub wpisz wiadomość
[14:25:31] ✅ Połączono! ID klienta: 550e8400...
> 
```

### Test 2: Wysyłanie wiadomości

#### W terminalu klienta
```
> Cześć serwer!
[14:25:35] 📤 Ty: Cześć serwer!
[14:25:35] 📥 Echo: Cześć serwer!
>
```

### Test 3: Status klienta

#### W terminalu klienta
```
> /status
[14:25:40] ℹ️ Status: Połączono ✅ | ID: 550e8400...
>
```

### Test 4: Wiele klientów

#### Terminal 1
```bash
python websocket_client.py --name "Klient-1"
```

#### Terminal 2 (nowy)
```bash
python websocket_client.py --name "Klient-2"
```

#### Terminal 3 (nowy)
```bash
# Sprawdź statystyki
curl http://localhost:8080/api/websocket/stats
```

Oczekiwany wynik:
```json
{
  "activeConnections": 2,
  "status": "OK"
}
```

### Test 5: Python Script do testowania

Utwórz plik `test_websocket.py`:

```python
#!/usr/bin/env python3
import json
import websocket
import time
import threading

def test_multiple_messages():
    """Testuje wysyłanie wielu wiadomości"""
    url = "ws://localhost:8080/ws/chat"
    
    def on_message(ws, msg):
        data = json.loads(msg)
        print(f"[{data['type']}] {data.get('message', '')}")
    
    ws = websocket.WebSocketApp(url, on_message=on_message)
    
    def send_messages():
        time.sleep(1)
        for i in range(5):
            msg = {"message": f"Test {i+1}"}
            ws.send(json.dumps(msg))
            time.sleep(0.5)
        ws.close()
    
    threading.Thread(target=send_messages, daemon=True).start()
    ws.run_forever()

if __name__ == "__main__":
    test_multiple_messages()
```

Uruchomienie:
```bash
python test_websocket.py
```

---

## Logowanie

### Lokalizacja logów

- **Serwer**: `logs/websocket.log`
- **Klient**: `client/client.log` (przy uruchomieniu)

### Konfiguracja logowania serwera (logback.xml)

```xml
<!-- Wysyłaj do konsoli (INFO) -->
<appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender"/>

<!-- Wysyłaj do pliku (DEBUG) z archiwizacją -->
<appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
  <file>${LOG_FILE}</file>
  <!-- Roluj codziennie lub przy 10MB -->
  <rollingPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedRollingPolicy">
    <fileNamePattern>${LOG_ARCHIVE_DIR}/websocket-%d{yyyy-MM-dd}.%i.log.gz</fileNamePattern>
    <maxFileSize>10MB</maxFileSize>
    <maxHistory>30</maxHistory>
  </rollingPolicy>
</appender>
```

### Przykład logów serwera

```
2026-03-17 14:25:30.123 [main] INFO  org.example.Main - Started Main in 3.456 seconds
2026-03-17 14:25:31.234 [nioEventLoopGroup-1-1] INFO  org.example.WebSocketHandler - New client connected: {"type":"connection","timestamp":"2026-03-17T14:25:31.234567","clientId":"550e8400-e29b-41d4-a716-446655440000","message":null}
2026-03-17 14:25:35.678 [nioEventLoopGroup-1-1] INFO  org.example.WebSocketHandler - Message received: {"type":"message","timestamp":"2026-03-17T14:25:35.678901","clientId":"550e8400-e29b-41d4-a716-446655440000","message":"Cześć serwer!"}
2026-03-17 14:25:35.789 [nioEventLoopGroup-1-1] INFO  org.example.WebSocketHandler - Sending echo: {"type":"echo","timestamp":"2026-03-17T14:25:35.789012","clientId":"550e8400-e29b-41d4-a716-446655440000","message":"Cześć serwer!"}
```

### Przykład logów klienta

```
2026-03-17 14:25:30 [INFO] WebSocket Client uruchomiony
2026-03-17 14:25:30 [INFO] Serwer: ws://localhost:8080/ws/chat
2026-03-17 14:25:31 [INFO] Połączenie z serwerem nawiązane
2026-03-17 14:25:31 [INFO] ✅ Połączono! ID klienta: 550e8400...
2026-03-17 14:25:35 [INFO] Wysłano wiadomość: {"type":"message",...}
2026-03-17 14:25:35 [DEBUG] Otrzymana wiadomość: {"type":"echo",...}
```

---

## Rozwiązywanie problemów

### Problem: "Nie można nawiązać połączenia"

**Przyczyna**: Serwer nie działa

**Rozwiązanie**:
```bash
# Sprawdź czy serwer działa
curl http://localhost:8080/api/websocket/stats

# Jeśli nie działa, uruchom go
./gradlew bootRun
```

### Problem: "ModuleNotFoundError: No module named 'websocket'"

**Przyczyna**: Brakuje biblioteki websocket-client

**Rozwiązanie**:
```bash
pip install websocket-client
# lub
pip3 install websocket-client
```

### Problem: "Connection refused"

**Przyczyna**: Serwer słucha na innym porcie/host

**Rozwiązanie**:
```bash
# Sprawdź czy serwer jest dostępny
netstat -tlnp | grep 8080  # Linux/Mac
netstat -ano | grep 8080   # Windows

# Zmień serwer w kliencie
python websocket_client.py --server ws://moj-serwer.com:8080/ws/chat
```

### Problem: "Timeout - nie udało się nawiązać połączenia"

**Przyczyna**: Serwer nie odpowiada w ciągu 5 sekund

**Rozwiązanie**:
```bash
# Zwiększ timeout edytując websocket_client.py
# Zmień linię: for _ in range(50):  # 5 sekund
#     na: for _ in range(150):      # 15 sekund
```

### Problem: "Port 8080 już w użyciu"

**Przyczyna**: Inny proces nasłuchuje na porcie 8080

**Rozwiązanie**:
```bash
# Maciej/Linux - zabij proces
lsof -i :8080
kill -9 <PID>

# Lub użyj innego portu w application.properties
# server.port=8081
```

---

## Struktura katalogów

```
webapp/
├── build.gradle.kts             # Konfiguracja Gradle
├── settings.gradle.kts
├── gradlew / gradlew.bat
├── gradle/
│   └── wrapper/
├── src/
│   └── main/
│       ├── java/org/example/
│       │   ├── Main.java
│       │   ├── WebSocketConfig.java
│       │   ├── WebSocketHandler.java
│       │   ├── WebSocketMessage.java
│       │   ├── WebSocketController.java
│       │   └── MathService.java
│       └── resources/
│           ├── logback.xml
│           └── static/
│               └── (puste - klient w Pythonie)
├── client/
│   ├── websocket_client.py        # Główny klient
│   ├── client.log                 # Logi (generowany)
│   └── test.json
├── doc/
│   ├── prompt-websocket.txt       # Wymagania
│   └── README.md                  # Ta dokumentacja
└── logs/
    └── websocket.log              # Logi serwera
```

---

## Sekcja zaawansowana

### Rozszerz WebSocket Handler

Aby dodać nowe funkcjonalności, edytuj `WebSocketHandler.java`:

```java
private void broadcastMessage(WebSocketMessage message, String excludeClientId) {
    // Ten kod wysyła wiadomość do wszystkich klientów
    // Możesz dodać filtrowanie, transformację itp.
}
```

### Dodaj nowe typy komunikatów

W `WebSocketMessage.java`:

```java
public enum MessageType {
    CONNECTION("connection"),
    DISCONNECTION("disconnection"),
    MESSAGE("message"),
    ECHO("echo"),
    ERROR("error"),              // Nowy typ
    NOTIFICATION("notification") // Nowy typ
}
```

### Metrics i monitoring

Użyj endpoint REST:
```bash
curl http://localhost:8080/api/websocket/stats
```

---

## Podsumowanie

Aplikacja WebSocket jest w pełni funkcjonalna i gotowa do użytku:
- ✅ Serwer WebSocket w Javie
- ✅ Klient w Pythonie
- ✅ Komunikaty JSON
- ✅ Logowanie
- ✅ Obsługa wielu klientów
- ✅ Dokumentacja

Aby zacząć, wykonaj:
```bash
# Terminal 1 - Serwer
./gradlew bootRun

# Terminal 2 - Klient
cd client && python websocket_client.py
```

Powodzenia! 🚀

