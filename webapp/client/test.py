#!/usr/bin/env python3
"""
Testy dla WebSocket Client
=============================

Skrypt zawiera verschiedne testy do weryfikacji poprawności działania
serwera WebSocket i klienta.

Uruchomienie:
    python test.py [test_name]

Dostępne testy:
    - test_connection: Test połączenia
    - test_echo: Test echo wiadomości
    - test_multiple_messages: Test wielu wiadomości
    - test_broadcast: Test broadcast do wielu klientów
"""

import websocket
import json
import time
import threading
import sys


class WebSocketTester:
    """Klasa do testowania WebSocket"""
    
    def __init__(self, url="ws://localhost:8080/ws/chat", name="Tester"):
        self.url = url
        self.name = name
        self.ws = None
        self.messages_received = []
        self.connected = False
    
    def on_open(self, ws):
        """Callback - połączenie otwarte"""
        self.connected = True
        print(f"[{self.name}] ✅ Połączono")
    
    def on_message(self, ws, message):
        """Callback - wiadomość otrzymana"""
        try:
            msg_data = json.loads(message)
            self.messages_received.append(msg_data)
            msg_type = msg_data.get('type', 'unknown')
            content = msg_data.get('message', '')
            print(f"[{self.name}] 📥 {msg_type}: {content}")
        except json.JSONDecodeError as e:
            print(f"[{self.name}] ❌ Błąd JSON: {e}")
    
    def on_error(self, ws, error):
        """Callback - błąd"""
        print(f"[{self.name}] ❌ Błąd: {error}")
    
    def on_close(self, ws, status_code, close_msg):
        """Callback - połączenie zamknięte"""
        self.connected = False
        print(f"[{self.name}] ✗ Rozłączono (kod: {status_code})")
    
    def connect(self):
        """Nawiąz połączenie"""
        print(f"[{self.name}] Łączenie z {self.url}...")
        self.ws = websocket.WebSocketApp(
            self.url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        
        # Uruchom w wątku
        ws_thread = threading.Thread(target=self.ws.run_forever, daemon=True)
        ws_thread.start()
        
        # Czekaj na połączenie
        for _ in range(50):
            if self.connected:
                return True
            time.sleep(0.1)
        
        return False
    
    def send(self, content):
        """Wyślij wiadomość"""
        try:
            msg = {"message": content}
            self.ws.send(json.dumps(msg, ensure_ascii=False))
            print(f"[{self.name}] 📤 Wysłano: {content}")
            return True
        except Exception as e:
            print(f"[{self.name}] ❌ Błąd wysyłania: {e}")
            return False
    
    def disconnect(self):
        """Rozłącz"""
        if self.ws:
            self.ws.close()
            self.connected = False
            print(f"[{self.name}] Rozłączono")


def test_connection():
    """Test 1: Nawiązanie połączenia"""
    print("\n" + "="*60)
    print("TEST 1: Nawiązanie połączenia")
    print("="*60)
    
    tester = WebSocketTester(name="Test1")
    if tester.connect():
        time.sleep(1)
        print("✅ Test przeszedł!")
        tester.disconnect()
        return True
    else:
        print("❌ Test nie przeszedł!")
        return False


def test_echo():
    """Test 2: Echo wiadomości"""
    print("\n" + "="*60)
    print("TEST 2: Echo wiadomości")
    print("="*60)
    
    tester = WebSocketTester(name="Test2")
    if not tester.connect():
        print("❌ Nie można nawiązać połączenia!")
        return False
    
    time.sleep(0.5)
    
    # Wyślij wiadomość
    tester.send("Test echo")
    time.sleep(1)
    
    # Sprawdź czy otrzymaliśmy echo
    echo_messages = [m for m in tester.messages_received if m.get('type') == 'echo']
    
    tester.disconnect()
    
    if echo_messages:
        print("✅ Test przeszedł!")
        return True
    else:
        print("❌ Nie otrzymano echo!")
        return False


def test_multiple_messages():
    """Test 3: Wysyłanie wielu wiadomości"""
    print("\n" + "="*60)
    print("TEST 3: Wysyłanie wielu wiadomości")
    print("="*60)
    
    tester = WebSocketTester(name="Test3")
    if not tester.connect():
        print("❌ Nie można nawiązać połączenia!")
        return False
    
    time.sleep(0.5)
    
    # Wyślij kilka wiadomości
    messages_to_send = ["Test 1", "Test 2", "Test 3"]
    for msg in messages_to_send:
        tester.send(msg)
        time.sleep(0.3)
    
    time.sleep(1)
    
    # Sprawdź odpowiedzi
    echo_count = len([m for m in tester.messages_received if m.get('type') == 'echo'])
    
    tester.disconnect()
    
    if echo_count >= len(messages_to_send):
        print(f"✅ Test przeszedł! Otrzymano {echo_count} echo.")
        return True
    else:
        print(f"❌ Brakuje echo! Wysłano: {len(messages_to_send)}, Otrzymano: {echo_count}")
        return False


def test_broadcast():
    """Test 4: Broadcast do wielu klientów"""
    print("\n" + "="*60)
    print("TEST 4: Broadcast do wielu klientów")
    print("="*60)
    
    # Połącz dwóch klientów
    client1 = WebSocketTester(name="Klient1")
    client2 = WebSocketTester(name="Klient2")
    
    if not client1.connect() or not client2.connect():
        print("❌ Nie można nawiązać połączenia!")
        return False
    
    time.sleep(0.5)
    
    # Wyślij wiadomość z client1
    client1.send("Broadcast test")
    time.sleep(1)
    
    # Sprawdź czy client2 otrzymał wiadomość
    client2_echo = [m for m in client2.messages_received if m.get('type') == 'echo']
    
    client1.disconnect()
    client2.disconnect()
    
    if client2_echo:
        print("✅ Test przeszedł! Broadcast działa.")
        return True
    else:
        print("❌ Broadcast nie działa!")
        return False


def test_json_format():
    """Test 5: Sprawdzenie formatu JSON"""
    print("\n" + "="*60)
    print("TEST 5: Sprawdzenie formatu JSON")
    print("="*60)
    
    tester = WebSocketTester(name="Test5")
    if not tester.connect():
        print("❌ Nie można nawiązać połączenia!")
        return False
    
    time.sleep(0.5)
    
    # Sprawdź strukturę wiadomości
    required_fields = {'type', 'timestamp', 'clientId'}
    
    if tester.messages_received:
        for msg in tester.messages_received:
            fields = set(msg.keys())
            if required_fields.issubset(fields):
                print(f"✅ Wiadomość ma wszystkie wymagane pola: {msg}")
            else:
                missing = required_fields - fields
                print(f"❌ Brakuje pól: {missing}")
                tester.disconnect()
                return False
    
    tester.send("Test formatu")
    time.sleep(0.5)
    
    tester.disconnect()
    
    print("✅ Test przeszedł!")
    return True


def run_all_tests():
    """Uruchom wszystkie testy"""
    print("\n" + "="*60)
    print("URUCHAMIANIE WSZYSTKICH TESTÓW")
    print("="*60)
    
    tests = [
        ("Połączenie", test_connection),
        ("Echo", test_echo),
        ("Wiele wiadomości", test_multiple_messages),
        ("Broadcast", test_broadcast),
        ("Format JSON", test_json_format),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Błąd w teście {test_name}: {e}")
            results.append((test_name, False))
        
        time.sleep(0.5)
    
    # Podsumowanie
    print("\n" + "="*60)
    print("PODSUMOWANIE TESTÓW")
    print("="*60)
    
    for test_name, result in results:
        status = "✅ PRZESZEDŁ" if result else "❌ NIE PRZESZEDŁ"
        print(f"{test_name}: {status}")
    
    total = len(results)
    passed = sum(1 for _, result in results if result)
    print(f"\nWynik: {passed}/{total} testów przeszło")
    
    return passed == total


def main():
    """Główna funkcja"""
    if len(sys.argv) > 1:
        test_name = sys.argv[1].lower()
        
        tests = {
            'connection': test_connection,
            'echo': test_echo,
            'multiple': test_multiple_messages,
            'broadcast': test_broadcast,
            'json': test_json_format,
        }
        
        if test_name in tests:
            test_func = tests[test_name]
            result = test_func()
            sys.exit(0 if result else 1)
        else:
            print(f"Nieznany test: {test_name}")
            print(f"Dostępne testy: {', '.join(tests.keys())}")
            sys.exit(1)
    else:
        # Uruchom wszystkie testy
        result = run_all_tests()
        sys.exit(0 if result else 1)


if __name__ == '__main__':
    main()

