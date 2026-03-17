# WebSocket - Szybki Start 🚀

Przewodnik do uruchomienia serwera WebSocket i klienta w 5 minut.

## Wymagania wstępne

- Java 17+
- Python 3.7+
- Terminal / Command Prompt

## Instalacja (jedna jedyna raz)

### 1. Python libraries
```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp
pip install websocket-client
# LUB
pip install -r requirements.txt
```

## Uruchomienie

### Terminal 1: Serwer WebSocket
```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp
./gradlew bootRun
```

Czekaj aż zobaczysz:
```
Started Main in X.XXX seconds
```

### Terminal 2: Klient WebSocket
```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp/client
python websocket_client.py
```

Powinieneś zobaczyć:
```
[14:25:30] ⚙️ Połączono jako: PythonClient
[14:25:30] ⚙️ Dostępne komendy: /status, /exit, lub wpisz wiadomość
[14:25:31] ✅ Połączono! ID klienta: 550e8400...
>
```

## Testowanie

### Wyślij wiadomość
```
> Cześć serwer!
[14:25:35] 📤 Ty: Cześć serwer!
[14:25:35] 📥 Echo: Cześć serwer!
>
```

### Sprawdź status
```
> /status
[14:25:40] ℹ️ Status: Połączono ✅ | ID: 550e8400...
>
```

### Wyjdź
```
> /exit
[14:25:45] ⚙️ Wychodzę...
```

## Zaawansowane

### Uruchom automatyczne testy
```bash
cd client
python test.py              # Wszystkie testy
python test.py connection   # Konkretny test
python test.py echo
python test.py broadcast
```

### Łącz się z innym serwerem
```bash
python websocket_client.py --server ws://192.168.1.100:8080/ws/chat
```

### Zmień nazwę klienta
```bash
python websocket_client.py --name "MojKlient"
```

## Logi

### Serwer
```bash
tail -f logs/websocket.log    # Linux/Mac
type logs/websocket.log       # Windows (ostatnich 100 linii)
```

### Klient
```bash
tail -f client/client.log     # Linux/Mac
```

## Rozwiązanie problemów

| Problem | Rozwiązanie |
|---------|-------------|
| "Nie można nawiązać połączenia" | Sprawdź czy serwer działa: `curl http://localhost:8080/api/websocket/stats` |
| "ModuleNotFoundError: websocket" | Zainstaluj: `pip install websocket-client` |
| "Port 8080 już w użyciu" | Zmień port w `application.properties` |

## Struktura

```
┌─────────────────────────┐
│   Java WebSocket Server │
│   ws://localhost:8080   │
└─────────────────────────┘
           ↕ (WebSocket)
┌─────────────────────────┐
│   Python WebSocket Client│
│   > Ty: Cześć!         │
│ ← Echo: Cześć!         │
└─────────────────────────┘
```

## Następne kroki

Przeczytaj pełną dokumentację: `doc/README.md`

---

**Potrzebujesz pomocy?** Sprawdź logi!

Serwer: `logs/websocket.log`
Klient: `client/client.log`

