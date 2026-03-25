#!/usr/bin/env python3
"""Przyklad klas komunikatow websocket i ich uzycia.

Skrypt laczy sie z serwerem i wysyla sekwencje:
1) STARTNEWGAME_REQUEST
2) ENDTURN_REQUEST
3) ENDGAME_REQUEST
"""

from __future__ import annotations

from dataclasses import dataclass, asdict, field
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

    def __init__(self, player_name: str, scenario: str):
        super().__init__(messageType="STARTNEWGAME_REQUEST")
        self.playerName = player_name
        self.scenario = scenario


@dataclass
class StartNewGameResponse(BaseMessage):
    createdGameId: str = ""
    serverStatus: str = ""


@dataclass
class EndTurnRequest(GameScopedMessage):
    playerId: str = ""
    turnNumber: int = 0

    def __init__(self, game_id: str, player_id: str, turn_number: int):
        super().__init__(messageType="ENDTURN_REQUEST", gameId=game_id)
        self.playerId = player_id
        self.turnNumber = turn_number


@dataclass
class EndTurnResponse(GameScopedMessage):
    accepted: bool = False
    nextPlayerId: str = ""


@dataclass
class EndGameRequest(GameScopedMessage):
    winnerId: str = ""
    reason: str = ""

    def __init__(self, game_id: str, winner_id: str, reason: str):
        super().__init__(messageType="ENDGAME_REQUEST", gameId=game_id)
        self.winnerId = winner_id
        self.reason = reason


@dataclass
class EndGameResponse(GameScopedMessage):
    ended: bool = False
    summary: str = ""


class DemoClient:
    def __init__(self, ws_url: str = "ws://localhost:8080/ws/chat") -> None:
        self.ws_url = ws_url
        self.ws: Optional[websocket.WebSocket] = None
        self.client_id: Optional[str] = None

    def connect(self) -> None:
        self.ws = websocket.create_connection(self.ws_url, timeout=5)
        raw = self.ws.recv()
        msg = json.loads(raw)
        self.client_id = msg.get("clientId")
        print("Polaczono:", msg)

    def send(self, message: BaseMessage) -> dict:
        if not self.ws:
            raise RuntimeError("Najpierw wykonaj connect()")
        message.clientId = self.client_id
        payload = json.dumps(asdict(message), ensure_ascii=False)
        self.ws.send(payload)
        raw_response = self.ws.recv()
        response = json.loads(raw_response)
        print("Odpowiedz:", response)
        return response

    def close(self) -> None:
        if self.ws:
            self.ws.close()
            self.ws = None


def main() -> None:
    client = DemoClient()
    client.connect()

    start_request = StartNewGameRequest(player_name="Anna", scenario="Moloch")
    start_response = client.send(start_request)
    game_id = start_response.get("createdGameId", "")

    end_turn_request = EndTurnRequest(game_id=game_id, player_id="Anna", turn_number=1)
    client.send(end_turn_request)

    end_game_request = EndGameRequest(game_id=game_id, winner_id="Anna", reason="Victory points")
    client.send(end_game_request)

    client.close()


if __name__ == "__main__":
    main()

