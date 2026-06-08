# from main.main import Game
# from main.communication.server_message import ServerMessage
# import json, os
# from pathlib import Path
# from main.utils.diff import Diff


# def view(data):
#     game = Game(data.gameState)
#     return game.build_user_view()

# def wczytaj(name):
#     current_dir = Path(__file__).parent
#     path = current_dir / name
#     # print(path)
#     with open(path, "r") as file:
#         data = file.read()
#     data = json.loads(data)
#     # print(data)
    
#     # print(type(data))
#     return ServerMessage(**data)

# def test1():
#     expected = {'state': {'factions': ['borgo', 'moloch'], 'board': [{'pos': [2, 4], 'unit': {'faction': 'borgo', 'name': 'sztab', 'rotation': 0, 'wired': False, 'ability_used': False, 'damage': 0}}], 'hands': {'borgo': {'tokens': ['sztab']}, 'moloch': {'tokens': []}}}, 'availableActions': {'hand': [False, False, False], 'board': [[2, 4]], 'buttons': []}, 'uiState': {'mode': 'rotation', 'message': '', 'faction': 'borgo'}}
#     data = wczytaj("data.json")
#     v = view(data)
#     print(v)
#     # assert False
#     assert v == expected, Diff.compare(v, expected)

# def test2():
#     data = wczytaj("data2.json")
#     v = view(data)
#     print(v["availableActions"])
#     # assert v == expected_view
#     # assert False

# def test3():
#     data = wczytaj("data3.json")
#     v = view(data)
#     print(v["availableActions"])
#     # assert False