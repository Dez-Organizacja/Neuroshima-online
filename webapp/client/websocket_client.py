#!/usr/bin/env python3
"""Klient Python dla websocket - utrzymuje połączenie z serwerem i umożliwia komunikację.

Funkcje:
- Logowanie przez REST i pobranie tokenu
- Łączenie się z serwerem websocket z nagłówkiem Authorization
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

try:
    import requests
except ModuleNotFoundError as exc:
    print("Brakuje biblioteki 'requests'. Zainstaluj zależności: pip install -r requirements.txt")
    raise SystemExit(1) from exc

try:
    import websocket
except ModuleNotFoundError as exc:
    print("Brakuje biblioteki 'websocket-client'. Zainstaluj zależności: pip install -r requirements.txt")
    raise SystemExit(1) from exc

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
        self.auth_token: Optional[str] = None
        self.on_message_callback = on_message_callback
        self.is_connected = False
        self.receive_thread: Optional[threading.Thread] = None
        self.stop_event = threading.Event()

    def login(self, auth_url: str, username: str, password: str) -> None:
        """Loguje użytkownika i pobiera token autoryzacyjny.

        Args:
            auth_url: URL endpointu logowania REST
            username: Nazwa użytkownika
            password: Hasło użytkownika
        """
        logger.info("Logowanie użytkownika %s przez %s", username, auth_url)
        response = requests.post(
            auth_url,
            json={"username": username, "password": password},
            timeout=5,
        )
        response.raise_for_status()
        data = response.json()
        token = data.get("token")
        if not token:
            raise RuntimeError("Serwer nie zwrócił tokenu podczas logowania")

        self.auth_token = token
        logger.info("Logowanie zakończone sukcesem. Użytkownik: %s", data.get("username", username))

    def connect(self) -> None:
        """Łączy się z serwerem websocket."""
        if not self.auth_token:
            raise RuntimeError("Brak tokenu autoryzacyjnego - wywołaj login() przed connect()")

        try:
            logger.info("Łączenie się z %s...", self.ws_url)
            headers = [f"Authorization: Bearer {self.auth_token}"]
            self.ws = websocket.create_connection(self.ws_url, timeout=5, header=headers)

            # Odebranie wiadomości powitalnej
            raw = self.ws.recv()
            hello = json.loads(raw)
            self.client_id = hello.get("clientId")
            # Timeout 5s ma służyć tylko etapowi połączenia; dalszy recv ma czekać na dane.
            self.ws.settimeout(None)
            self.stop_event.clear()
            self.is_connected = True
            
            logger.info("Połączono pomyślnie. ClientId: %s", self.client_id)
            logger.info("Wiadomość serwera: %s", hello)

            # Uruchomienie wątku do nasłuchiwania wiadomości
            self.receive_thread = threading.Thread(target=self._receive_loop, daemon=True)
            self.receive_thread.start()
            
        except Exception as e:
            logger.error("Błąd podczas połączenia: %s", e)
            self.is_connected = False
            raise

    def _receive_loop(self) -> None:
        """Pętla nasłuchiwania wiadomości z serwera."""
        while self.is_connected and self.ws and not self.stop_event.is_set():
            try:
                message = self.ws.recv()
                if message:
                    logger.info("Odebrano wiadomość: %s", message)
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
                logger.error("Błąd podczas odbierania wiadomości: %s", e)
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
            logger.info("Wysyłanie wiadomości: %s", json_message)
            self.ws.send(json_message)
        except Exception as e:
            logger.error("Błąd podczas wysyłania wiadomości: %s", e)
            raise

    def send_json_string(self, json_string: str) -> None:
        """Wysyła surowy string JSON do serwera.
        
        Args:
            json_string: String JSON do wysłania
        """
        if not self.ws or not self.is_connected:
            raise RuntimeError("Brak aktywnego połączenia z serwerem")
        
        try:
            logger.info("Wysyłanie wiadomości: %s", json_string)
            self.ws.send(json_string)
        except Exception as e:
            logger.error("Błąd podczas wysyłania wiadomości: %s", e)
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
                logger.error("Błąd podczas zamykania połączenia: %s", e)
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
        "--auth-url",
        default="http://localhost:8080/api/auth/login",
        help="Adres endpointu logowania REST"
    )
    parser.add_argument("--username", required=True, help="Login użytkownika")
    parser.add_argument("--password", required=True, help="Hasło użytkownika")
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
        client.login(args.auth_url, args.username, args.password)
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
        logger.error("Błąd: %s", e)
        sys.exit(1)
    finally:
        client.close()


if __name__ == "__main__":
    main()
