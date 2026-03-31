#!/usr/bin/env python3
"""Przykladowe payloady komunikatow gry.

Uwaga: jedyna implementacja klienta WebSocket jest w websocket_client.py.
Ten plik generuje jedynie JSON-y testowe bez laczenia z serwerem.
"""

from __future__ import annotations

from dataclasses import asdict
import json

from websocket_client import CreateNewRoomRequest, EndGameRequest, StartNewGameRequest


def build_payload_examples() -> list[dict]:
    room_id = "room-1"
    player_id = "Anna"
    game_id = "example-game-id"

    return [
        asdict(CreateNewRoomRequest(room_id=room_id, player_name=player_id)),
        asdict(StartNewGameRequest(room_id=room_id, player_id=player_id, scenario="Moloch")),
        asdict(EndGameRequest(game_id=game_id, winner_id=player_id, reason="Victory points")),
    ]


def main() -> None:
    for payload in build_payload_examples():
        print(json.dumps(payload, ensure_ascii=False))


if __name__ == "__main__":
    main()

