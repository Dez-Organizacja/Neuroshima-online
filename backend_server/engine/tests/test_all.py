from main.main import Game
from main.communication.server_message import ServerMessage
import json
from pathlib import Path

expected_state = {'state': {'factions': ['borgo', 'moloch'], 'board': [], 'hands': {'borgo': {'tokens': ['bitwa', 'nozownik', 'medyk']}, 'moloch': {'tokens': []}}}, 'availableActions': {'hand': [False, False, False], 'board': [[0, 2], [0, 4], [0, 6], [1, 1], [1, 3], [1, 5], [1, 7], [2, 0], [2, 2], [2, 4], [2, 6], [2, 8], [3, 1], [3, 3], [3, 5], [3, 7], [4, 2], [4, 4], [4, 6]], 'buttons': ['cancel', 'discard']}, 'uiState': {'mode': 'default', 'message': '', 'faction': 'borgo'}}

def test_all():
    current_dir = Path(__file__).parent
    path = current_dir / "data.json"
    with open(path, "r") as file:
        data = file.read()

    data = json.loads(data)
    
    # print(type(data))
    data = ServerMessage(**data)
    # print(data)
    game = Game(data.gameState)
    game.handle_action(data.userAction)
    # print(game.build_user_view())
    # print(expected_state)
    assert expected_state == game.build_user_view()