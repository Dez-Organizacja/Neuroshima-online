#!/usr/bin/env python3
"""Prosty test manualny nowego protokolu websocket.

Wymaga uruchomionego serwera na ws://localhost:8080/ws/chat.
"""

import json

import websocket


def main() -> None:
    ws = websocket.create_connection("ws://localhost:8080/ws/chat", timeout=5)

    hello = json.loads(ws.recv())
    print("CONNECTED:", hello)
    client_id = hello.get("clientId")

    start_payload = {
        "messageType": "STARTNEWGAME_REQUEST",
        "clientId": client_id,
        "playerName": "Tester",
        "scenario": "Moloch",
    }
    ws.send(json.dumps(start_payload, ensure_ascii=False))
    start_response = json.loads(ws.recv())
    print("START RESPONSE:", start_response)

    game_id = start_response.get("createdGameId")
    if not game_id:
        raise RuntimeError("Brak createdGameId")

    end_turn_payload = {
        "messageType": "ENDTURN_REQUEST",
        "clientId": client_id,
        "gameId": game_id,
        "playerId": "Tester",
        "turnNumber": 1,
    }
    ws.send(json.dumps(end_turn_payload, ensure_ascii=False))
    end_turn_response = json.loads(ws.recv())
    print("ENDTURN RESPONSE:", end_turn_response)

    end_game_payload = {
        "messageType": "ENDGAME_REQUEST",
        "clientId": client_id,
        "gameId": game_id,
        "winnerId": "Tester",
        "reason": "Test finished",
    }
    ws.send(json.dumps(end_game_payload, ensure_ascii=False))
    end_game_response = json.loads(ws.recv())
    print("ENDGAME RESPONSE:", end_game_response)

    ws.close()


if __name__ == "__main__":
    main()

