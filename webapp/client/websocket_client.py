#!/usr/bin/env python3
"""Klient Python dla nowych komunikatow websocket.

Obslugiwane typy:
- STARTNEWGAME_REQUEST/RESPONSE
- ENDTURN_REQUEST/RESPONSE
- ENDGAME_REQUEST/RESPONSE
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass, field
from datetime import datetime
import json
from typing import Optional

import websocket


@dataclass
class BaseMessage:
    messageType: str
    clientId: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class GameScopedMessage(BaseMessage):
    gameId: str = ""


@dataclass
class StartNewGameRequest(BaseMessage):
    playerName: str = ""
    scenario: str = ""

    def __init__(self, player_name: str, scenario: str) -> None:
        super().__init__(messageType="STARTNEWGAME_REQUEST")
        self.playerName = player_name
        self.scenario = scenario


@dataclass
class EndTurnRequest(GameScopedMessage):
    playerId: str = ""
    turnNumber: int = 0

    def __init__(self, game_id: str, player_id: str, turn_number: int) -> None:
        super().__init__(messageType="ENDTURN_REQUEST", gameId=game_id)
        self.playerId = player_id
        self.turnNumber = turn_number


@dataclass
class EndGameRequest(GameScopedMessage):
    winnerId: str = ""
    reason: str = ""

    def __init__(self, game_id: str, winner_id: str, reason: str) -> None:
        super().__init__(messageType="ENDGAME_REQUEST", gameId=game_id)
        self.winnerId = winner_id
        self.reason = reason


class WebSocketGameClient:
    def __init__(self, ws_url: str) -> None:
        self.ws_url = ws_url
        self.ws: Optional[websocket.WebSocket] = None
        self.client_id: Optional[str] = None

    def connect(self) -> None:
        self.ws = websocket.create_connection(self.ws_url, timeout=5)
        raw = self.ws.recv()
        hello = json.loads(raw)
        self.client_id = hello.get("clientId")
        print("CONNECTED", hello)

    def send(self, message: BaseMessage) -> dict:
        if not self.ws:
            raise RuntimeError("Brak aktywnego polaczenia")
        message.clientId = self.client_id
        self.ws.send(json.dumps(asdict(message), ensure_ascii=False))
        raw = self.ws.recv()
        response = json.loads(raw)
        print("RESPONSE", response)
        return response

    def close(self) -> None:
        if self.ws:
            self.ws.close()
            self.ws = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Klient websocket dla protokolu gry")
    parser.add_argument("--server", default="ws://localhost:8080/ws/chat", help="Adres serwera websocket")
    parser.add_argument("--player", default="Anna", help="Nazwa gracza")
    parser.add_argument("--scenario", default="Moloch", help="Scenariusz dla STARTNEWGAME")
    parser.add_argument("--turn", type=int, default=1, help="Numer tury dla ENDTURN")
    parser.add_argument("--reason", default="Victory points", help="Powod zakonczenia gry")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    client = WebSocketGameClient(args.server)
    client.connect()

    start_response = client.send(StartNewGameRequest(player_name=args.player, scenario=args.scenario))
    game_id = start_response.get("createdGameId", "")
    if not game_id:
        raise RuntimeError("Brak createdGameId w odpowiedzi STARTNEWGAME_RESPONSE")

    client.send(EndTurnRequest(game_id=game_id, player_id=args.player, turn_number=args.turn))
    client.send(EndGameRequest(game_id=game_id, winner_id=args.player, reason=args.reason))
    client.close()


if __name__ == "__main__":
    main()
