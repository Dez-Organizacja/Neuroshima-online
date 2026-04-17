# import pytest
# import os
# import sys
# from copy import deepcopy

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from akcje import Actions
# from main import Game
# from variable import *
# from zeton import Zeton

# width = 5
# length = 9
# available_actions_structure = {
#                           UI.HAND: {'moloch': [False, False, False], 'borgo': [False, False, False]}, 
#                           UI.BOARD: [[False for _ in range(length)] for _ in range(width)], 
#                           UI.BOTTOM: {
#                               Bottom.END_TURN: False, 
#                               Bottom.DISCARD: False, 
#                               Bottom.USE: False, 
#                               Bottom.CANCEL: False, 
#                               Bottom.YES: False, 
#                               Bottom.NO: False}
#                               }
# default_game_state = {'faza': Turn.Type.STANDARD, 
#                       'frakcje' : ['moloch', 'borgo'],
#                       'state': State.NO_SELECTION, 
#                       'selected': None, 
#                       'current_frakcja': 'moloch', 
#                       'active_action': None,
#                       'next_turns': [
#                           {Turn.FRACTION: 'moloch', Turn.TYPE: 'tura'}, 
#                           {Turn.FRACTION: 'borgo', Turn.TYPE: 'tura'}
#                           ], 
#                       'board': [[None for _ in range(length)] for _ in range(width)], 
#                       'pile': {"moloch" : [], 'borgo': []}, 
#                       'hand': {'moloch': [], 'borgo': []}, 
#                       'available_actions': available_actions_structure
#                     }

# def test_bitwa_selected():
#     data = deepcopy(default_game_state)
#     data["hand"]["moloch"].append("bitwa")
#     data["action"] = {Action.Key.TYPE : UI.HAND, Action.Key.SLOT : 0}
#     data["available_actions"][UI.HAND]["moloch"][0] = True
#     game = Game(data)

#     assert(game.state == State.SELECTED_HAND)
#     assert(game.selected[Action.Key.SLOT] == 0)
#     assert(game.active_action == Token.Type.Instant.BITWA)

#     correct_actions = deepcopy(available_actions_structure)
#     correct_actions[UI.BOTTOM][Bottom.CANCEL] = True
#     correct_actions[UI.BOTTOM][Bottom.USE] = True

# def test_bitwa_use():
#     data = deepcopy(default_game_state)
#     data["hand"]["moloch"].append("bitwa")
#     data["action"] = {Action.Key.TYPE : UI.BOTTOM, Action.Key.BOTTOM : Bottom.USE}
#     data["state"] = State.SELECTED_HAND
#     data["selected"] = {Selected.SLOT : 0, Selected.NAME : Token.Type.Instant.BITWA}
#     data["active_action"] = Token.Type.Instant.BITWA
#     data["available_actions"][UI.BOTTOM][Bottom.USE] = True
#     data["next_turns"] = [{Turn.FRACTION : "moloch", Turn.TYPE : Turn.Type.STANDARD}, {Turn.FRACTION : "borgo", Turn.TYPE : Turn.Type.STANDARD}]
#     game = Game(data)

#     assert(game.state == State.NO_SELECTION)
#     assert(game.selected == None)
#     assert(game.active_action == None)
#     assert(game.current_frakcja == "borgo")
#     assert(game.hand["moloch"] == [])

# def check_available_actions(active_hand, active_bottoms, active_hexes, output):
#     for fraction in output[UI.HAND]:
#         for slot in output[UI.HAND][fraction]:
#             status = output[UI.HAND][fraction][slot]
#             assert((fraction, slot) in active_hand) == status
    
#     for bottom in output[UI.BOTTOM]:
#         status = output[UI.BOTTOM][bottom]
#         assert(bottom in active_bottoms) == status
        
#     for x in range(width):
#         for y in range(length):
#             status = output[UI.BOARD][x][y]
#             assert((x, y) in active_hexes) == status


# def test_ruch_selected():
#     data = deepcopy(default_game_state)
#     data["hand"]["moloch"].append("ruch")
#     data["board"][1][1] = Zeton.clear_token("sieciarz", "borgo")
#     data["board"][1][1][Token.ROTATION] = 1
#     data["board"][1][3] = Zeton.clear_token("mutek", "borgo")
#     data["board"][2][4] = Zeton.clear_token("sztab", "borgo")

#     data["board"][2][2] = Zeton.clear_token("klaun", "moloch")
#     data["board"][2][0] = Zeton.clear_token("sztab", "moloch")
#     data["action"] = None
#     game = Game(data)
#     data = game.export_game_state()
#     data["action"] = {Action.Key.TYPE : UI.HAND, Action.Key.SLOT : 0}
#     game = Game(data)
#     # data["available_actions"][UI.HAND]["moloch"][0] = True

#     assert(game.state == State.SELECTED_HAND)
#     assert(game.selected[Selected.SLOT] == 0)
#     assert(game.selected[Selected.NAME] == Token.Type.Instant.MOVE)

#     output = game.available_actions
#     active_hand = []
#     active_bottoms = [Bottom.DISCARD, Bottom.CANCEL]
#     active_hexes = [(2, 2)]
#     # print(output)
#     check_available_actions(active_hand, active_bottoms, active_hexes, output)
    

# def test_ruch_selected2():
#     data = deepcopy(default_game_state)
#     data["hand"]["moloch"].append("ruch")
#     data["board"][1][1] = Zeton.clear_token("sieciarz", "borgo")
#     data["board"][1][1][Token.ROTATION] = 1
#     data["board"][1][3] = Zeton.clear_token("mutek", "borgo")
#     data["board"][2][4] = Zeton.clear_token("sztab", "borgo")

#     data["board"][2][2] = Zeton.clear_token("klaun", "moloch")
#     data["board"][2][0] = Zeton.clear_token("sztab", "moloch")
#     data["state"] = State.SELECTED_HAND
#     data["selected"] = {Selected.SLOT : 0, Selected.NAME : Token.Type.Instant.MOVE}
#     data["active_action"] = Token.Type.Instant.MOVE
#     data["action"] = None
#     # game = Game(data)
#     data = Game(data).export_game_state()
#     data["action"] = {Action.Key.TYPE : UI.BOARD, Action.Key.X : 2, Action.Key.Y : 2}
#     game = Game(data)
#     # data["available_actions"][UI.BOARD][2][2] = True

#     assert(game.state == State.MOVING)
#     assert(game.selected[Selected.X] == 2)
#     assert(game.selected[Selected.Y] == 2)
#     assert(game.selected[Selected.NAME] == "klaun")

#     output = game.available_actions
#     # print(output)
#     active_hand = []
#     active_bottoms = [Bottom.CANCEL]
#     active_hexes = [(3, 1), (3, 3), (2, 2)]
#     check_available_actions(active_hand, active_bottoms, active_hexes, output)

# def test_ruch3():
#     data = deepcopy(default_game_state)
#     data["hand"]["moloch"].append("ruch")
#     data["state"] = State.MOVING
#     data["selected"] = {Selected.NAME : "klaun", Selected.X : 2, Selected.Y : 2}
#     data["action"] = None
#     data["active_action"] = Token.Type.Instant.MOVE

#     data["board"][1][1] = Zeton.clear_token("sieciarz", "borgo")
#     data["board"][1][1][Token.ROTATION] = 1
#     data["board"][1][3] = Zeton.clear_token("mutek", "borgo")
#     data["board"][2][4] = Zeton.clear_token("sztab", "borgo")

#     data["board"][2][2] = Zeton.clear_token("klaun", "moloch")
#     data["board"][2][0] = Zeton.clear_token("sztab", "moloch")
#     data = Game(data).export_game_state()
#     data["action"] = {Action.Key.TYPE : UI.BOARD, Action.Key.X : 3, Action.Key.Y : 3}
#     game = Game(data)

#     assert(game.state == State.ROTATE)
#     assert(game.selected[Selected.NAME] == "klaun")
#     assert(game.selected[Selected.X] == 3)
#     assert(game.selected[Selected.Y] == 3)
#     assert(game.board.board[2][2] == None)
#     zeton = game.board.board[3][3].zeton_to_json()
#     assert(zeton[Token.NAME] == "klaun")
#     assert(zeton[Token.FRACTION] == "moloch")
#     assert(zeton[Token.DAMAGE] == 0)
#     assert(zeton[Token.WIRED] == False)
#     assert(zeton[Token.ROTATION] == 0)
#     assert(game.hand["moloch"] == [])

#     output = game.available_actions
#     active_hand = []
#     active_bottoms = []
#     active_hexes = [(3, 3)]
#     check_available_actions(active_hand, active_bottoms, active_hexes, output)

# def test_bomb_selected():
#     data = deepcopy(default_game_state)
#     data["hand"]["moloch"].append(Token.Type.Instant.BOMB)
#     data["action"] = {Action.Key.TYPE : UI.HAND, Action.Key.SLOT : 0}
#     data["available_actions"][UI.HAND]["moloch"][0] = True
#     game = Game(data)

#     assert(game.state == State.SELECTED_HAND)
#     assert(game.selected[Action.Key.SLOT] == 0)
#     assert(game.active_action == Token.Type.Instant.BOMB)

#     output = game.available_actions
#     # print(output)
#     active_hand = []
#     active_bottoms = [Bottom.DISCARD, Bottom.CANCEL]
#     active_hexes = [(1, 3), (1, 5), (2, 2), (2, 4), (2, 6), (3, 3), (3, 5)]
#     check_available_actions(active_hand, active_bottoms, active_hexes, output)

# def test_bomb_use():
#     data = deepcopy(default_game_state)
#     data["hand"]["moloch"].append(Token.Type.Instant.BOMB)
#     data["action"] = None
#     data["state"] = State.SELECTED_HAND
#     data["selected"] = {Selected.SLOT : 0, Selected.NAME : Token.Type.Instant.BOMB}
#     data["active_action"] = Token.Type.Instant.BOMB
#     # data["next_turns"] = [{Turn.FRACTION : "moloch", Turn.TYPE : Turn.Type.STANDARD}, {Turn.FRACTION : "borgo", Turn.TYPE : Turn.Type.STANDARD}]
    
#     data["board"][1][1] = Zeton.clear_token("sieciarz", "borgo")
#     data["board"][1][3] = Zeton.clear_token("mutek", "borgo")
#     data["board"][2][4] = Zeton.clear_token("sztab", "borgo")

#     data["board"][2][2] = Zeton.clear_token("klaun", "moloch")
#     data["board"][2][0] = Zeton.clear_token("sztab", "moloch")
#     data = Game(data).export_game_state()
#     data["action"] = {Action.Key.TYPE : UI.BOARD, Action.Key.X : 1, Action.Key.Y : 3}
#     game = Game(data)
    
#     assert(game.state == State.NO_SELECTION)
#     assert(game.selected == None)
#     assert(game.active_action == None)
#     assert(game.hand["moloch"] == [])
#     assert(game.board.board[1][1] == None)
#     assert(game.board.board[1][3] == None)
#     zeton = game.board.board[2][4]
#     assert(zeton.rany == 0)
#     zeton = game.board.board[2][2]
#     assert(zeton.rany == 1)

# def test_grenade_selected():
#     data = deepcopy(default_game_state)
#     data["hand"]["borgo"].append(Token.Type.Instant.GRENADE)
#     data["action"] = {Action.Key.TYPE : UI.HAND, Action.Key.SLOT : 0}
#     data["available_actions"][UI.HAND]["borgo"][0] = True
#     data["current_frakcja"] = "borgo"

#     data["board"][1][3] = Zeton.clear_token("mutek", "borgo")
#     data["board"][1][5] = Zeton.clear_token("sieciarz", "moloch")
#     data["board"][2][2] = Zeton.clear_token("klaun", "moloch")
#     data["board"][2][4] = Zeton.clear_token("sztab", "borgo")
#     data["board"][2][6] = Zeton.clear_token("sztab", "moloch")
#     game = Game(data)

#     assert(game.state == State.SELECTED_HAND)
#     assert(game.selected[Action.Key.SLOT] == 0)
#     assert(game.active_action == Token.Type.Instant.GRENADE)

#     output = game.available_actions
#     # print(output)
#     active_hand = []
#     active_bottoms = [Bottom.DISCARD, Bottom.CANCEL]
#     active_hexes = [(1, 5), (2, 2)]
#     check_available_actions(active_hand, active_bottoms, active_hexes, output)

# def test_grenade_use():
#     data = deepcopy(default_game_state)
#     data["hand"]["borgo"].append(Token.Type.Instant.GRENADE)
#     data["state"] = State.SELECTED_HAND
#     data["selected"] = {Selected.SLOT : 0, Selected.NAME : Token.Type.Instant.GRENADE}
#     data["active_action"] = Token.Type.Instant.GRENADE
#     data["action"] = None
#     data["current_frakcja"] = "borgo"

#     data["board"][1][3] = Zeton.clear_token("mutek", "borgo")
#     data["board"][1][5] = Zeton.clear_token("sieciarz", "moloch")
#     data["board"][2][2] = Zeton.clear_token("klaun", "moloch")
#     data["board"][2][4] = Zeton.clear_token("sztab", "borgo")
#     data["board"][2][6] = Zeton.clear_token("sztab", "moloch")
#     data = Game(data).export_game_state()
#     data["action"] = {Action.Key.TYPE : UI.BOARD, Action.Key.X : 2, Action.Key.Y : 2}
#     game = Game(data)

#     assert(game.state == State.NO_SELECTION)
#     assert(game.selected == None)
#     assert(game.active_action == None)
#     assert(game.hand["borgo"] == [])
#     assert(game.board.board[2][2] == None)

# def test_sniper_selected():
#     data = deepcopy(default_game_state)
#     data["hand"] = {'moloch': [], 'testowa': []}
#     data["available_actions"][UI.HAND] = {'moloch': [False, False, False], 'testowa': [False, False, False]}
#     data["hand"]["testowa"].append(Token.Type.Instant.SNIPER)
#     data["action"] = {Action.Key.TYPE : UI.HAND, Action.Key.SLOT : 0}
#     data["available_actions"][UI.HAND]["testowa"][0] = True
#     data["frakcje"] = ["testowa", "moloch"]
#     data["current_frakcja"] = "testowa"

#     data["board"][2][2] = Zeton.clear_token("klaun", "moloch")
#     data["board"][0][6] = Zeton.clear_token("sieciarz", "moloch")
#     data["board"][2][0] = Zeton.clear_token("sztab", "moloch")
#     data["board"][4][2] = Zeton.clear_token("sieciarz", "testowa")
#     game = Game(data)

#     assert(game.state == State.SELECTED_HAND)
#     assert(game.selected[Action.Key.SLOT] == 0)
#     assert(game.active_action == Token.Type.Instant.SNIPER)

#     output = game.available_actions
#     # print(output)
#     active_hand = []
#     active_bottoms = [Bottom.DISCARD, Bottom.CANCEL]
#     active_hexes = [(2, 2), (0, 6)]
#     check_available_actions(active_hand, active_bottoms, active_hexes, output)

# def test_sniper_use():
#     data = deepcopy(default_game_state)
#     data["hand"] = {'moloch': [], 'testowa': []}
#     data["available_actions"][UI.HAND] = {'moloch': [False, False, False], 'testowa': [False, False, False]}
#     data["hand"]["testowa"].append(Token.Type.Instant.SNIPER)
#     data["frakcje"] = ["testowa", "moloch"]
#     data["current_frakcja"] = "testowa"
#     data["state"] = State.SELECTED_HAND
#     data["selected"] = {Selected.SLOT : 0, Selected.NAME : Token.Type.Instant.SNIPER}
#     data["active_action"] = Token.Type.Instant.SNIPER
#     data["action"] = None

#     data["board"][2][2] = Zeton.clear_token("klaun", "moloch")
#     data["board"][0][6] = Zeton.clear_token("sieciarz", "moloch")
#     data["board"][2][0] = Zeton.clear_token("sztab", "moloch")
#     data["board"][4][2] = Zeton.clear_token("sieciarz", "testowa")
#     data = Game(data).export_game_state()
#     data["action"] = {Action.Key.TYPE : UI.BOARD, Action.Key.X : 2, Action.Key.Y : 2}
#     game = Game(data)

#     assert(game.state == State.NO_SELECTION)
#     assert(game.selected == None)
#     assert(game.active_action == None)
#     assert(game.hand["testowa"] == [])
#     zeton = game.board.board[2][2]
#     assert(zeton.rany == 1)

# def test_push_selected():
#     data = deepcopy(default_game_state)
#     data["hand"]["moloch"].append(Token.Type.Instant.PUSH)
#     data["board"][1][1] = Zeton.clear_token("sieciarz", "borgo")
#     data["board"][1][1][Token.ROTATION] = 1
#     data["board"][3][1] = Zeton.clear_token("mutek", "borgo")
#     data["board"][2][4] = Zeton.clear_token("sztab", "borgo")

#     data["board"][2][2] = Zeton.clear_token("klaun", "moloch")
#     data["board"][2][0] = Zeton.clear_token("sztab", "moloch")
#     data["action"] = None
    
#     game = Game(data)
#     data = game.export_game_state()
#     data["action"] = {Action.Key.TYPE : UI.HAND, Action.Key.SLOT : 0}
#     game = Game(data)

#     assert(game.state == State.SELECTED_HAND)
#     assert(game.selected[Selected.SLOT] == 0)
#     assert(game.selected[Selected.NAME] == Token.Type.Instant.PUSH)

#     output = game.available_actions
#     active_hand = []
#     active_bottoms = [Bottom.DISCARD, Bottom.CANCEL]
#     active_hexes = [(2, 2)]
#     # print(output)
#     check_available_actions(active_hand, active_bottoms, active_hexes, output)
    

# def test_push_selected2():
#     data = deepcopy(default_game_state)
#     data["hand"]["moloch"].append(Token.Type.Instant.PUSH)
#     data["board"][1][1] = Zeton.clear_token("sieciarz", "borgo")
#     data["board"][1][1][Token.ROTATION] = 1
#     data["board"][3][1] = Zeton.clear_token("mutek", "borgo")
#     data["board"][2][4] = Zeton.clear_token("sztab", "borgo")

#     data["board"][2][2] = Zeton.clear_token("klaun", "moloch")
#     data["board"][2][0] = Zeton.clear_token("sztab", "moloch")
#     data["board"][4][2] = Zeton.clear_token("sieciarz", "moloch")

#     data["action"] = None
#     data["state"] = State.SELECTED_HAND
#     data["selected"] = {Selected.SLOT : 0, Selected.NAME : Token.Type.Instant.PUSH}
#     data["active_action"] = Token.Type.Instant.PUSH
#     # data["action"] = None
#     # game = Game(data)
#     data = Game(data).export_game_state()
#     data["action"] = {Action.Key.TYPE : UI.BOARD, Action.Key.X : 2, Action.Key.Y : 2}
#     game = Game(data)
#     # data["available_actions"][UI.BOARD][2][2] = True

#     assert(game.state == State.SELECTED_PUSHER)
#     assert(game.selected[Selected.X] == 2)
#     assert(game.selected[Selected.Y] == 2)
#     assert(game.selected[Selected.NAME] == "klaun")

#     output = game.available_actions
#     print(output)
#     active_hand = []
#     active_bottoms = [Bottom.CANCEL]
#     active_hexes = [(1, 1), (2, 4)]
#     check_available_actions(active_hand, active_bottoms, active_hexes, output)

# def test_push_target_selected():
#     data = deepcopy(default_game_state)
#     data["hand"]["moloch"].append(Token.Type.Instant.PUSH)
#     data["board"][1][1] = Zeton.clear_token("sieciarz", "borgo")
#     data["board"][1][1][Token.ROTATION] = 1
#     data["board"][3][1] = Zeton.clear_token("mutek", "borgo")
#     data["board"][2][4] = Zeton.clear_token("sztab", "borgo")

#     data["board"][2][2] = Zeton.clear_token("klaun", "moloch")
#     data["board"][2][0] = Zeton.clear_token("sztab", "moloch")
#     data["board"][4][2] = Zeton.clear_token("sieciarz", "moloch")

#     data["action"] = None
#     data["state"] = State.SELECTED_PUSHER
#     data["selected"] = {Selected.X : 2, Selected.Y : 2, Selected.NAME : "klaun"}
#     data["active_action"] = Token.Type.Instant.PUSH
#     # data["current_frakcja"] = "borgo"
#     data = Game(data).export_game_state()
#     data["action"] = {Action.Key.TYPE : UI.BOARD, Action.Key.X : 1, Action.Key.Y : 1}
#     game = Game(data)

#     assert(game.state == State.PUSHING)
#     assert(game.selected[Selected.NAME] == "sieciarz")
#     assert(game.selected[Selected.X] == 1)
#     assert(game.selected[Selected.Y] == 1)
#     assert(game.current_frakcja == "borgo")
#     output = game.available_actions
#     active_hand = []
#     active_bottoms = []
#     active_hexes = [(0, 2)]
#     check_available_actions(active_hand, active_bottoms, active_hexes, output)


# def test_push_use():
#     data = deepcopy(default_game_state)
#     data["hand"]["moloch"].append(Token.Type.Instant.PUSH)
#     data["board"][1][1] = Zeton.clear_token("sieciarz", "borgo")
#     data["board"][1][1][Token.ROTATION] = 1
#     data["board"][3][1] = Zeton.clear_token("mutek", "borgo")
#     data["board"][2][4] = Zeton.clear_token("sztab", "borgo")

#     data["board"][2][2] = Zeton.clear_token("klaun", "moloch")
#     data["board"][2][0] = Zeton.clear_token("sztab", "moloch")
#     data["board"][4][2] = Zeton.clear_token("sieciarz", "moloch")

#     data["action"] = None
#     data["state"] = State.PUSHING
#     data["selected"] = {Selected.X : 1, Selected.Y : 1, Selected.PUSHER_X : 2, Selected.PUSHER_Y : 2, Selected.NAME : "sieciarz"}
#     data["active_action"] = Token.Type.Instant.PUSH
#     data["current_frakcja"] = "borgo"

#     data = Game(data).export_game_state()
#     data["action"] = {Action.Key.TYPE : UI.BOARD, Action.Key.X : 0, Action.Key.Y : 2}
#     game = Game(data)

#     assert(game.state == State.NO_SELECTION)
#     assert(game.selected == None)
#     assert(game.active_action == None)
#     assert(game.board.board[1][1] == None)
#     zeton = game.board.board[0][2]
#     assert(zeton.nazwa == "sieciarz")
#     assert(zeton.frakcja == "borgo")
#     assert(zeton.rotacja == 1)
#     assert(game.hand["moloch"] == [])
#     assert(game.current_frakcja == "moloch")