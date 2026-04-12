import pytest
import os
import sys
from copy import deepcopy

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from akcje import Actions
from main import Game
from variable import *
from zeton import Zeton

width = 5
length = 9
available_actions_structure = {
                          UI.HAND: {'moloch': [False, False, False], 'borgo': [False, False, False]}, 
                          UI.BOARD: [[False for _ in range(length)] for _ in range(width)], 
                          UI.BOTTOM: {
                              Bottom.END_TURN: False, 
                              Bottom.DISCARD: False, 
                              Bottom.USE: False, 
                              Bottom.CANCEL: False, 
                              Bottom.YES: False, 
                              Bottom.NO: False}
                              }
default_game_state = {'faza': Turn.Type.STANDARD, 'state': State.NO_SELECTION, 'selected': None, 'current_frakcja': 'moloch', 
                      'next_turns': [
                          {Turn.FRACTION: 'moloch', Turn.TYPE: 'tura'}, 
                          {Turn.FRACTION: 'borgo', Turn.TYPE: 'tura'}
                          ], 
                      'board': [[None for _ in range(length)] for _ in range(width)], 
                      'pile': {"moloch" : [], 'borgo': []}, 
                      'hand': {'moloch': [], 'borgo': []}, 
                      'available_actions': available_actions_structure
                    }

def test_bitwa_selected():
    data = deepcopy(default_game_state)
    data["hand"]["moloch"].append("bitwa")
    data["action"] = {Action.Key.TYPE : UI.HAND, Action.Key.SLOT : 0}
    data["available_actions"][UI.HAND]["moloch"][0] = True
    game = Game(data)

    assert(game.state == State.SELECTED_HAND)
    assert(game.selected[Action.Key.SLOT] == 0)

    correct_actions = deepcopy(available_actions_structure)
    correct_actions[UI.BOTTOM][Bottom.CANCEL] = True
    correct_actions[UI.BOTTOM][Bottom.USE] = True

def test_bitwa_use():
    data = deepcopy(default_game_state)
    data["hand"]["moloch"].append("bitwa")
    data["action"] = {Action.Key.TYPE : UI.BOTTOM, Action.Key.BOTTOM : Bottom.USE}
    data["state"] = State.SELECTED_HAND
    data["selected"] = {Selected.SLOT : 0, Selected.NAME : Token.Type.Instant.BITWA}
    data["available_actions"][UI.BOTTOM][Bottom.USE] = True
    data["next_turns"] = [{Turn.FRACTION : "moloch", Turn.TYPE : Turn.Type.STANDARD}, {Turn.FRACTION : "borgo", Turn.TYPE : Turn.Type.STANDARD}]
    game = Game(data)

    assert(game.state == State.NO_SELECTION)
    assert(game.selected == None)
    assert(game.current_frakcja == "borgo")

def check_available_actions(active_hand, active_bottoms, active_hexes, output):
    for fraction in output[UI.HAND]:
        for slot in output[UI.HAND][fraction]:
            status = output[UI.HAND][fraction][slot]
            assert((fraction, slot) in active_hand) == status
    
    for bottom in output[UI.BOTTOM]:
        status = output[UI.BOTTOM][bottom]
        assert(bottom in active_bottoms) == status
        
    for x in range(width):
        for y in range(length):
            status = output[UI.BOARD][x][y]
            assert((x, y) in active_hexes) == status


def test_ruch_selected():
    data = deepcopy(default_game_state)
    data["hand"]["moloch"].append("ruch")
    data["board"][1][1] = Zeton.clear_token("sieciarz", "borgo")
    data["board"][1][1][Token.ROTATION] = 1
    data["board"][1][3] = Zeton.clear_token("mutek", "borgo")
    data["board"][2][4] = Zeton.clear_token("sztab", "borgo")

    data["board"][2][2] = Zeton.clear_token("klaun", "moloch")
    data["board"][2][0] = Zeton.clear_token("sztab", "moloch")
    data["action"] = None
    game = Game(data)
    data = game.export_game_state()
    data["action"] = {Action.Key.TYPE : UI.HAND, Action.Key.SLOT : 0}
    game = Game(data)
    # data["available_actions"][UI.HAND]["moloch"][0] = True

    assert(game.state == State.SELECTED_HAND)
    assert(game.selected[Selected.SLOT] == 0)
    assert(game.selected[Selected.NAME] == Token.Type.Instant.MOVE)

    output = game.available_actions
    active_hand = []
    active_bottoms = [Bottom.DISCARD, Bottom.CANCEL]
    active_hexes = [(2, 2)]
    # print(output)
    check_available_actions(active_hand, active_bottoms, active_hexes, output)
    

def test_ruch_selected2():
    data = deepcopy(default_game_state)
    data["hand"]["moloch"].append("ruch")
    data["board"][1][1] = Zeton.clear_token("sieciarz", "borgo")
    data["board"][1][1][Token.ROTATION] = 1
    data["board"][1][3] = Zeton.clear_token("mutek", "borgo")
    data["board"][2][4] = Zeton.clear_token("sztab", "borgo")

    data["board"][2][2] = Zeton.clear_token("klaun", "moloch")
    data["board"][2][0] = Zeton.clear_token("sztab", "moloch")
    data["state"] = State.SELECTED_HAND
    data["selected"] = {Selected.SLOT : 0, Selected.NAME : Token.Type.Instant.MOVE}
    data["action"] = None
    # game = Game(data)
    data = Game(data).export_game_state()
    data["action"] = {Action.Key.TYPE : UI.BOARD, Action.Key.X : 2, Action.Key.Y : 2}
    game = Game(data)
    # data["available_actions"][UI.BOARD][2][2] = True

    assert(game.state == State.MOVING)
    assert(game.selected[Selected.X] == 2)
    assert(game.selected[Selected.Y] == 2)
    assert(game.selected[Selected.NAME] == "klaun")

    output = game.available_actions
    # print(output)
    active_hand = []
    active_bottoms = [Bottom.CANCEL]
    active_hexes = [(3, 1), (3, 3)]
    check_available_actions(active_hand, active_bottoms, active_hexes, output)

def test_ruch3():
    data = deepcopy(default_game_state)
    data["hand"]["moloch"].append("ruch")
    data["state"] = State.MOVING
    data["selected"] = {Selected.NAME : "klaun", Selected.X : 2, Selected.Y : 2}
    data["action"] = None

    data["board"][1][1] = Zeton.clear_token("sieciarz", "borgo")
    data["board"][1][1][Token.ROTATION] = 1
    data["board"][1][3] = Zeton.clear_token("mutek", "borgo")
    data["board"][2][4] = Zeton.clear_token("sztab", "borgo")

    data["board"][2][2] = Zeton.clear_token("klaun", "moloch")
    data["board"][2][0] = Zeton.clear_token("sztab", "moloch")
    data = Game(data).export_game_state()
    data["action"] = {Action.Key.TYPE : UI.BOARD, Action.Key.X : 3, Action.Key.Y : 3}
    game = Game(data)

    assert(game.state == State.ROTATE)
    assert(game.selected[Selected.NAME] == "klaun")
    assert(game.selected[Selected.X] == 3)
    assert(game.selected[Selected.Y] == 3)
    assert(game.board.board[2][2] == None)
    zeton = game.board.board[3][3].zeton_to_json()
    assert(zeton[Token.NAME] == "klaun")
    assert(zeton[Token.FRACTION] == "moloch")
    assert(zeton[Token.DAMAGE] == 0)
    assert(zeton[Token.WIRED] == False)
    assert(zeton[Token.ROTATION] == 0)

    output = game.available_actions
    active_hand = []
    active_bottoms = []
    active_hexes = [(3, 3)]
    check_available_actions(active_hand, active_bottoms, active_hexes, output)    