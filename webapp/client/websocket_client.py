#!/usr/bin/env python3
"""Klient Python dla websocket - utrzymuje połączenie z serwerem i umożliwia komunikację.

Funkcje:
- Łączenie się z serwerem websocket
- Utrzymywanie aktywnego połączenia
- Wysyłanie wiadomości JSON
- Odbieranie wiadomości JSON
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import threading
from typing import Optional, Callable

import websocket
from user_input_handlers import on_user_input, user_input_loop

# Konfiguracja logowania
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WebSocketGameClient:
    """Klient websocket do komunikacji z serwerem gry."""

    def __init__(
        self,
        ws_url: str,
        on_message_callback: Optional[Callable[[str], None]] = None,
    ) -> None:
        """Inicjalizacja klienta websocket.
        
        Args:
            ws_url: URL serwera websocket (np. ws://localhost:8080/ws/chat)
            on_message_callback: Opcjonalna funkcja wywoływana gdy odebrano wiadomość
        """
        self.ws_url = ws_url
        self.ws: Optional[websocket.WebSocket] = None
        self.client_id: Optional[str] = None
        self.on_message_callback = on_message_callback
        self.is_connected = False
        self.receive_thread: Optional[threading.Thread] = None
        self.stop_event = threading.Event()

    def connect(self) -> None:
        """Łączy się z serwerem websocket."""
        try:
            logger.info(f"Łączenie się z {self.ws_url}...")
            self.ws = websocket.create_connection(self.ws_url, timeout=5)
            
            # Odebranie wiadomości powitalnej
            raw = self.ws.recv()
            hello = json.loads(raw)
            self.client_id = hello.get("clientId")
            # Timeout 5s ma służyć tylko etapowi połączenia; dalszy recv ma czekać na dane.
            self.ws.settimeout(None)
            self.stop_event.clear()
            self.is_connected = True
            
            logger.info(f"Połączono pomyślnie. ClientId: {self.client_id}")
            logger.info(f"Wiadomość serwera: {hello}")
            
            # Uruchomienie wątku do nasłuchiwania wiadomości
            self.receive_thread = threading.Thread(target=self._receive_loop, daemon=True)
            self.receive_thread.start()
            
        except Exception as e:
            logger.error(f"Błąd podczas połączenia: {e}")
            self.is_connected = False
            raise

    def _receive_loop(self) -> None:
        """Pętla nasłuchiwania wiadomości z serwera."""
        while self.is_connected and self.ws and not self.stop_event.is_set():
            try:
                message = self.ws.recv()
                if message:
                    logger.info(f"Odebrano wiadomość: {message}")
                    if self.on_message_callback:
                        self.on_message_callback(message)
            except websocket.WebSocketTimeoutException:
                # Gdyby timeout został ustawiony gdziekolwiek indziej, nie zrywaj połączenia.
                continue
            except websocket.WebSocketConnectionClosedException:
                logger.warning("Połączenie zostało zamknięte przez serwer")
                self.is_connected = False
                self.stop_event.set()
                break
            except Exception as e:
                logger.error(f"Błąd podczas odbierania wiadomości: {e}")
                self.is_connected = False
                self.stop_event.set()
                break

    def send(self, message: dict) -> None:
        """Wysyła wiadomość JSON do serwera.
        
        Args:
            message: Słownik z wiadomością do wysłania
        """
        if not self.ws or not self.is_connected:
            raise RuntimeError("Brak aktywnego połączenia z serwerem")
        
        try:
            # Dodaj clientId do wiadomości jeśli istnieje
            if self.client_id and "clientId" not in message:
                message["clientId"] = self.client_id
            
            json_message = json.dumps(message, ensure_ascii=False)
            logger.info(f"Wysyłanie wiadomości: {json_message}")
            self.ws.send(json_message)
        except Exception as e:
            logger.error(f"Błąd podczas wysyłania wiadomości: {e}")
            raise

    def send_json_string(self, json_string: str) -> None:
        """Wysyła surowy string JSON do serwera.
        
        Args:
            json_string: String JSON do wysłania
        """
        if not self.ws or not self.is_connected:
            raise RuntimeError("Brak aktywnego połączenia z serwerem")
        
        try:
            logger.info(f"Wysyłanie wiadomości: {json_string}")
            self.ws.send(json_string)
        except Exception as e:
            logger.error(f"Błąd podczas wysyłania wiadomości: {e}")
            raise

    def is_alive(self) -> bool:
        """Sprawdza czy połączenie jest aktywne."""
        return self.is_connected and self.ws is not None

    def close(self) -> None:
        """Zamyka połączenie z serwerem."""
        self.stop_event.set()
        self.is_connected = False
        if self.ws:
            try:
                logger.info("Zamykanie połączenia...")
                self.ws.close()
            except Exception as e:
                logger.error(f"Błąd podczas zamykania połączenia: {e}")
            finally:
                self.ws = None



def parse_args() -> argparse.Namespace:
    """Parsowanie argumentów linii poleceń."""
    parser = argparse.ArgumentParser(
        description="Klient websocket do komunikacji z serwerem gry Neuroshima"
    )
    parser.add_argument(
        "--server",
        default="ws://localhost:8080/ws/chat",
        help="Adres serwera websocket (domyślnie: ws://localhost:8080/ws/chat)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Tryb verbose (więcej logów)"
    )
    return parser.parse_args()


def main() -> None:
    """Główna funkcja - łączy się z serwerem i utrzymuje połączenie."""
    args = parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    def on_message(msg: str) -> None:
        """Callback dla odebranych wiadomości."""
        print(f"\n>>> WIADOMOŚĆ Z SERWERA: {msg}")
    
    client = WebSocketGameClient(args.server, on_message_callback=on_message)
    
    try:
        client.connect()
        logger.info("Połączenie ustanowione. Naciśnij Ctrl+C aby wyjść.")
        logger.info("Możesz wpisywać dane w terminalu - hook on_user_input() będzie wywoływany.")

        input_thread = threading.Thread(target=user_input_loop, args=(client,), daemon=True)
        input_thread.start()

        while client.is_alive() and not client.stop_event.is_set():
            threading.Event().wait(0.2)

    except KeyboardInterrupt:
        logger.info("\nPrzerwano przez użytkownika")
    except Exception as e:
        logger.error(f"Błąd: {e}")
        sys.exit(1)
    finally:
        client.close()


if __name__ == "__main__":
    main()
