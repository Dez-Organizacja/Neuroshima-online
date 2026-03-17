#!/usr/bin/env python3
"""
WebSocket Client dla aplikacji Neuroshima
================================================

Prosty klient WebSocket, który łączy się z serwerem WebSocket i umożliwia:
- Nawiązywanie połączenia z serwerem
- Wysyłanie wiadomości
- Odbieranie odpowiedzi
- Graceful disconnection

Wymagania:
    - Python 3.7+
    - websocket-client (instalacja: pip install websocket-client)

Użycie:
    python websocket_client.py [--server WS_URL] [--name CLIENT_NAME]
    
    Domyślne parametry:
    - WS_URL: ws://localhost:8080/ws/chat
    - CLIENT_NAME: PythonClient

Przykłady:
    # Połączenie z domyślnym serwerem
    python websocket_client.py
    
    # Połączenie z innym serwerem
    python websocket_client.py --server ws://192.168.1.100:8080/ws/chat
    
    # Podaj nazwę klienta
    python websocket_client.py --name "Bot-1"
"""

import websocket
import json
import time
import threading
import uuid
import logging
from datetime import datetime
from argparse import ArgumentParser
import sys


# ===== KONFIGURACJA LOGOWANIA =====
def setup_logging(log_file="client.log"):
    """
    Konfiguruje logowanie dla klienta.
    
    Ustawia format logów i zapisuje je zarówno do konsoli jak i pliku.
    
    Args:
        log_file (str): Ścieżka do pliku logów
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Format dla logów
    log_format = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Handler do pliku
    try:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(log_format)
        logger.addHandler(file_handler)
    except Exception as e:
        print(f"Nie można otworzyć pliku logów: {e}")

    # Handler do konsoli
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    return logger


# ===== GŁÓWNA KLASA KLIENTA =====
class WebSocketClient:
    """
    Klient WebSocket do komunikacji z serwerem WebSocket.
    
    Atrybuty:
        server_url (str): URL serwera WebSocket
        client_name (str): Nazwa klienta do wyświetlania
        client_id (str): Unikalny identyfikator klienta (generowany przez serwer)
        ws (websocket.WebSocket): Obiekt WebSocket
        connected (bool): Status połączenia
        logger (logging.Logger): Logger do logowania zdarzeń
        running (bool): Flaga wskazująca czy pętla odbierająca powinna działać
    """

    def __init__(self, server_url="ws://localhost:8080/ws/chat", client_name="PythonClient", logger=None):
        """
        Inicjalizuje klienta WebSocket.
        
        Args:
            server_url (str): URL serwera WebSocket
            client_name (str): Nazwa klienta
            logger (logging.Logger): Logger do logowania
        """
        self.server_url = server_url
        self.client_name = client_name
        self.client_id = None
        self.ws = None
        self.connected = False
        self.logger = logger or logging.getLogger(__name__)
        self.running = False

    def connect(self):
        """
        Nawiązuje połączenie z serwerem WebSocket.
        
        Obsługuje:
        - ustanowienie połączenia
        - callback dla otwarcia połączenia
        - callback dla odbierania wiadomości
        - callback dla błędów
        - callback dla zamknięcia połączenia
        
        Returns:
            bool: True jeśli połączenie się powiodło, False w innym wypadku
        """
        try:
            self.logger.info(f"Łączenie z serwerem: {self.server_url}")
            
            self.ws = websocket.WebSocketApp(
                self.server_url,
                on_open=self._on_open,
                on_message=self._on_message,
                on_error=self._on_error,
                on_close=self._on_close
            )
            
            # Uruchom pętlę WebSocket w osobnym wątku
            self.running = True
            ws_thread = threading.Thread(target=self.ws.run_forever, daemon=True)
            ws_thread.start()
            
            # Czekaj na nawiązanie połączenia (max 5 sekund)
            for _ in range(50):
                if self.connected:
                    return True
                time.sleep(0.1)
            
            self.logger.error("Timeout - nie udało się nawiązać połączenia")
            return False
            
        except Exception as e:
            self.logger.error(f"Błąd połączenia: {e}")
            return False

    def _on_open(self, ws):
        """
        Callback wywoływany gdy WebSocket się otworzy.
        
        Args:
            ws (websocket.WebSocket): Obiekt WebSocket
        """
        self.logger.info("Połączenie z serwerem nawiązane")

    def _on_message(self, ws, message):
        """
        Callback wywoływany gdy klient odbierze wiadomość.
        
        Parsuje JSON i loguje wiadomość, a następnie wyświetla ją
        w zależności od typu.
        
        Args:
            ws (websocket.WebSocket): Obiekt WebSocket
            message (str): Wiadomość w formacie JSON
        """
        try:
            msg_data = json.loads(message)
            msg_type = msg_data.get('type', 'unknown')
            content = msg_data.get('message', '')
            timestamp = msg_data.get('timestamp', '')
            client_id = msg_data.get('clientId', '')
            
            # Loguj wiadomość
            self.logger.debug(f"Otrzymana wiadomość: {message}")
            
            # Obsłuż różne typy komunikatów
            if msg_type == 'connection':
                self.client_id = client_id
                self.connected = True
                self.logger.info(f"✅ Połączono! ID klienta: {self.client_id[:8]}...")
                self._print_message(f"Połączono z serwerem (ID: {self.client_id[:8]}...)", "system")
                
            elif msg_type == 'echo':
                self._print_message(f"Echo: {content}", "received")
                
            elif msg_type == 'disconnection':
                self.logger.info(f"⚠️ Rozłączono: {content}")
                self._print_message(f"Serwer: {content}", "system")
                
            elif msg_type == 'message':
                self._print_message(f"Serwer: {content}", "received")
                
            else:
                self.logger.warning(f"Nieznany typ wiadomości: {msg_type}")
                self._print_message(f"Wiadomość ({msg_type}): {content}", "received")
                
        except json.JSONDecodeError as e:
            self.logger.error(f"Błąd parsowania JSON: {e}")
            self._print_message(f"Błąd: {message}", "error")

    def _on_error(self, ws, error):
        """
        Callback wywoływany gdy WebSocket napotkał błąd.
        
        Args:
            ws (websocket.WebSocket): Obiekt WebSocket
            error: Błąd
        """
        self.logger.error(f"❌ Błąd WebSocket: {error}")
        self._print_message(f"Błąd: {error}", "error")

    def _on_close(self, ws, close_status_code, close_msg):
        """
        Callback wywoływany gdy WebSocket się zamknie.
        
        Args:
            ws (websocket.WebSocket): Obiekt WebSocket
            close_status_code (int): Kod zamknięcia
            close_msg (str): Wiadomość zamknięcia
        """
        self.connected = False
        self.running = False
        self.logger.info(f"Połączenie zamknięte (kod: {close_status_code})")
        self._print_message("Rozłączono od serwera", "system")

    def send_message(self, content):
        """
        Wysyła wiadomość do serwera.
        
        Wiadomość jest wysyłana w formacie JSON z polem "message".
        Jeśli klient nie jest połączony, wyświetli komunikat błędu.
        
        Args:
            content (str): Treść wiadomości
            
        Returns:
            bool: True jeśli wysłanie się powiodło, False w innym wypadku
        """
        if not self.connected or not self.ws:
            self.logger.warning("Nie jest możliwe wysłanie - brak połączenia z serwerem")
            self._print_message("Nie można wysłać - brak połączenia", "error")
            return False

        try:
            # Utwórz wiadomość w formacie JSON
            message = {
                "type": "message",
                "message": content,
                "timestamp": datetime.now().isoformat(),
                "clientId": self.client_id or "unknown"
            }
            
            # Wyślij wiadomość
            self.ws.send(json.dumps(message, ensure_ascii=False))
            
            # Loguj wysłaną wiadomość
            self.logger.info(f"Wysłano wiadomość: {json.dumps(message, ensure_ascii=False)}")
            self._print_message(f"Ty: {content}", "sent")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Błąd wysyłania wiadomości: {e}")
            self._print_message(f"Błąd wysyłania: {e}", "error")
            return False

    def disconnect(self):
        """
        Rozłącza się z serwerem.
        
        Zatrzymuje pętlę WebSocket i zamyka połączenie.
        """
        if self.ws:
            self.logger.info("Rozłączanie z serwerem...")
            self.running = False
            self.ws.close()
            self.connected = False
            self._print_message("Rozłączanie...", "system")

    def _print_message(self, message, msg_type="info"):
        """
        Wyświetla wiadomość w konsoli z odpowiednim formatowaniem.
        
        Args:
            message (str): Treść wiadomości
            msg_type (str): Typ wiadomości (info, sent, received, system, error)
        """
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        # Emoji i kolory dla różnych typów
        type_icons = {
            'info': 'ℹ️',
            'sent': '📤',
            'received': '📥',
            'system': '⚙️',
            'error': '❌'
        }
        
        icon = type_icons.get(msg_type, '•')
        print(f"[{timestamp}] {icon} {message}")

    def run_interactive(self):
        """
        Uruchamia tryb interaktywny klienta.
        
        Pozwala użytkownikowi na:
        - Wpisanie wiadomości i wysłanie jej (Enter)
        - Wyświetlenie statusu (/status)
        - Wyjście (/exit lub Ctrl+C)
        """
        self._print_message(f"Połączono jako: {self.client_name}", "system")
        self._print_message("Dostępne komendy: /status, /exit, lub wpisz wiadomość", "system")
        
        try:
            while self.running and self.connected:
                try:
                    user_input = input("> ").strip()
                    
                    if not user_input:
                        continue
                    
                    # Obsłuż komendy
                    if user_input.startswith('/'):
                        self._handle_command(user_input)
                    else:
                        # Wyślij zwykłą wiadomość
                        self.send_message(user_input)
                        
                except EOFError:
                    # Ctrl+D
                    self._print_message("Koniec wejścia", "system")
                    break
                except KeyboardInterrupt:
                    # Ctrl+C
                    print()
                    self._print_message("Przerwano przez użytkownika", "system")
                    break
                    
        except Exception as e:
            self.logger.error(f"Błąd w trybie interaktywnym: {e}")
            self._print_message(f"Błąd: {e}", "error")
        finally:
            self.disconnect()

    def _handle_command(self, command):
        """
        Obsługuje komendy specjalne.
        
        Obsługiwane komendy:
        - /status: wyświetli status połączenia
        - /exit: zamknie połączenie i wyjdzie
        - /help: wyświetli pomoc
        
        Args:
            command (str): Komenda do obsłużenia
        """
        cmd = command.lower().strip()
        
        if cmd == '/status':
            status = "Połączono ✅" if self.connected else "Rozłączono ❌"
            client_info = f"ID: {self.client_id[:8]}..." if self.client_id else "Brak ID"
            self._print_message(f"Status: {status} | {client_info}", "info")
            
        elif cmd == '/exit':
            self._print_message("Wychodzę...", "system")
            self.disconnect()
            self.running = False
            
        elif cmd == '/help':
            self._print_message("Dostępne komendy:", "info")
            self._print_message("  /status - wyświetl status połączenia", "info")
            self._print_message("  /exit - wyjdź", "info")
            self._print_message("  /help - wyświetl tę wiadomość", "info")
            
        else:
            self._print_message(f"Nieznana komenda: {cmd}", "error")


# ===== MAIN =====
def main():
    """
    Główna funkcja uruchamiająca klienta.
    
    Parsuje argumenty wiersza poleceń i uruchamia klienta w trybie interaktywnym.
    """
    parser = ArgumentParser(
        description='WebSocket Client dla aplikacji Neuroshima'
    )
    parser.add_argument(
        '--server',
        default='ws://localhost:8080/ws/chat',
        help='URL serwera WebSocket (domyślnie: ws://localhost:8080/ws/chat)'
    )
    parser.add_argument(
        '--name',
        default='PythonClient',
        help='Nazwa klienta (domyślnie: PythonClient)'
    )
    parser.add_argument(
        '--log',
        default='client.log',
        help='Plik logów (domyślnie: client.log)'
    )
    
    args = parser.parse_args()
    
    # Skonfiguruj logowanie
    logger = setup_logging(args.log)
    logger.info("=" * 60)
    logger.info("WebSocket Client uruchomiony")
    logger.info(f"Serwer: {args.server}")
    logger.info(f"Nazwa klienta: {args.name}")
    logger.info("=" * 60)
    
    # Utwórz i uruchom klienta
    client = WebSocketClient(
        server_url=args.server,
        client_name=args.name,
        logger=logger
    )
    
    # Spróbuj się połączyć
    if client.connect():
        # Uruchom tryb interaktywny
        client.run_interactive()
    else:
        logger.error("Nie udało się nawiązać połączenia z serwerem")
        print("❌ Nie udało się nawiązać połączenia z serwerem")
        sys.exit(1)


if __name__ == '__main__':
    main()


