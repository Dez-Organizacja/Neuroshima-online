from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from websocket_client import WebSocketGameClient

logger = logging.getLogger(__name__)


def on_user_input(client: "WebSocketGameClient", user_text: str) -> None:
    wejscie = user_text.strip().split()
    if not wejscie:
        return

    typ = wejscie[0].upper()
    if (typ == "JOINROOM"):
        if len(wejscie) < 3:
            logger.warning("Uzycie: JOINROOM <roomId> <playerName>")
            return

        message = {
            "messageType": "JOINROOM_REQUEST",
            "roomId": wejscie[1],
            "playerName": wejscie[2],
        }

        try:
            client.send(message)
            logger.info("Wyslano JOINROOM_REQUEST")
        except Exception as e:
            logger.error(f"Nie udalo sie wyslac JOINROOM_REQUEST: {e}")

    elif (typ == "CREATEROOM"):
        if len(wejscie) < 3:
            logger.warning("Uzycie: CREATEROOM <roomId> <playerName>")
            return

        message = {
            "messageType": "CREATENEWROOM_REQUEST",
            "roomId": wejscie[1],
            "playerName": wejscie[2],
        }

        try:
            client.send(message)
            logger.info("Wyslano CREATEROOM_REQUEST")
        except Exception as e:
            logger.info(f"pokoj sie nie stworzyl: {e}")

    elif (typ == "LEAVEROOM"):
        if len(wejscie) < 3:
            logger.warning("Uzycie: LEAVEROOM <roomId> <playerName>")
            return

        message = {
            "messageType": "LEAVEROOM_REQUEST",
            "roomId": wejscie[1],
            "playerName": wejscie[2],
        }

        try:
            client.send(message)
            logger.info("Wyslano LEAVEROOM_REQUEST")
        except Exception as e:
            logger.info(f"nie wyszedles z pokoju: {e}")

    elif (typ == "ROOMSTATUS"):
        if len(wejscie) < 2:
            logger.warning("Uzycie: GETROOMSTATUS <roomId>")

        message = {
            "messageType": "GETROOMSTATUS_REQUEST",
            "roomId": wejscie[1],
        }

        try:
            client.send(message)
            logger.info("Wyslano GETROOMSTATUS_REQUEST")
        except Exception as e:
            logger.info(f"nie wyszedles z pokoju: {e}")

    elif (typ == "NEWGAME"):
        if(len(wejscie) < 4):
            logger.warning("Uzycie: NEWGAME <roomId>")
            return

        message = {
            "messageType": "NEWGAME_REQUEST",
            "roomId": wejscie[1],
            "scenario": {
                "frakcje": {
                    "player1": wejscie[2],
                    "player2": wejscie[3],
                }
            }
           }

        try:
            client.send(message)
            logger.info("Wyslano NEWGAME_REQUEST")
        except Exception as e:
            logger.info(f"nie udalo sie stworzyc nowej gry: {e}")

    else:
        logger.warning(f"Nieznana komenda: {typ}")
    return

def user_input_loop(client: "WebSocketGameClient") -> None:
    """Pętla odczytu wejścia z terminala działająca równolegle z odbiorem WS."""
    while client.is_alive() and not client.stop_event.is_set():
        try:
            user_text = input()
        except EOFError:
            logger.info("Koniec wejścia (EOF) - zamykanie klienta")
            client.stop_event.set()
            break
        except Exception as e:
            logger.error(f"Błąd wejścia użytkownika: {e}")
            client.stop_event.set()
            break

        on_user_input(client, user_text)

