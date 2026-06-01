from main.main import Game
from main.communication.server_message import ServerMessage
import json, os
from pathlib import Path

expected_view = {'state': {'factions': ['moloch', 'borgo'], 'board': [{'pos': [2, 4], 'unit': {'name': 'lowca', 'faction': 'moloch', 'ROTATION': 0, 'DAMAGE': 0, 'WIRED': False, 'ability_used': False, 'clever_iniciative': {'initiative': [[3, False, True]], 'is_blocked_to_0': False, 'iniciative_boosts': 0, 'num_of_new': 0}}}, {'pos': [2, 6], 'unit': {'name': 'klaun', 'faction': 'moloch', 'ROTATION': 0, 'DAMAGE': 0, 'WIRED': False, 'ability_used': False, 'clever_iniciative': {'initiative': [[2, False, True]], 'is_blocked_to_0': False, 'iniciative_boosts': 0, 'num_of_new': 0}}}, {'pos': [1, 5], 'unit': {'name': 'sztab', 'faction': 'borgo', 'ROTATION': 0, 'DAMAGE': 0, 'WIRED': False, 'ability_used': False, 'clever_iniciative': {'initiative': [[0, False, True]], 'is_blocked_to_0': False, 'iniciative_boosts': 0, 'num_of_new': 0}}}, {'pos': [3, 3], 'unit': {'name': 'mutek', 'faction': 'borgo', 'ROTATION': 0, 'DAMAGE': 0, 'WIRED': False, 'ability_used': False, 'clever_iniciative': {'initiative': [[2, False, True]], 'is_blocked_to_0': False, 'iniciative_boosts': 0, 'num_of_new': 0}}}], 'hands': {'borgo': {'tokens': []}, 'moloch': {'tokens': ['opancerzonylowca', 'bitwa', 'odepchniecie']}}}, 'availableActions': {'hand': [False, False, False], 'board': [[2, 4], [2, 6]], 'buttons': ['discard', 'cancel']}, 'uiState': {'mode': 'default', 'message': '', 'faction': 'moloch'}}

def view(data):
    game = Game(data.gameState)
    return game.build_user_view()

def wczytaj(name):
    current_dir = Path(__file__).parent
    path = current_dir / name
    # print(path)
    with open(path, "r") as file:
        data = file.read()
    data = json.loads(data)
    # print(data)
    
    # print(type(data))
    return ServerMessage(**data)

def test1():
    data = wczytaj("data.json")
    v = view(data)
    assert v == expected_view
    # assert False