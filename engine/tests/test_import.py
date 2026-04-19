import pytest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from variable import * 
from main import Game

def test_start_game():
    data = {
        'fractions' : ['moloch', 'borgo'],
        'phase' : 'newgame'
    }
    game = Game(data)
    state = game.state

    assert(state.phase == Phase.GAME)
    assert(state.selected == {})
    assert(state.active_action == {})
    assert(state.current_fraction in state.fractions)
    for fraction in state.fractions:
        assert(fraction in data['fractions'])
    assert(len(state.fractions) == len(data['fractions']))
    
    for turn in state.next_turns:
        assert(turn[Turn.FRACTION] in data['fractions'])
        assert(turn[Turn.TYPE] == Turn.Type.HQ_PLACEMENT)
    
    for fraction in state.fractions:
        player_state = state.players[fraction]
        assert(player_state.hand.tokens == [])
        assert(player_state.hand.active_token == None)
        assert(len(player_state.pile.tokens) > 0)

def test_import_game_state():
    data = {
        'fractions' : ['moloch', 'borgo'],
        'phase' : 'newgame'
    }
    game = Game(data)
    data = game.state.to_dict()
    # print(data)

    data['players']['moloch']['hand']['tokens'].append('klaun')
    data['players']['moloch']['hand']['active_token'] = 0
    data['players']['moloch']['pile'].remove('klaun')
    data['players']['moloch']['pile'].remove('sztab')
    data['board']['board'][2][2] = {Token.FRACTION : "moloch", Token.NAME : "sztab", Token.ROTATION : 1, Token.DAMAGE : 0, Token.WIRED : False}
    data['selected'] = {Selected.NAME : "klaun", Selected.SLOT : 0}
    data['state'] = State.SELECTED_HAND

    game = Game(data)
    state = game.state
    # print(state.to_dict())
    state.print_game_state()
    assert(state.phase == Phase.GAME)
    assert(state.selected == {Selected.NAME : "klaun", Selected.SLOT : 0})
    assert(state.active_action == {})
    assert(state.current_fraction in state.fractions)
    for fraction in state.fractions:
        assert(fraction in data['fractions'])
    assert(len(state.fractions) == len(data['fractions']))
    
    for turn in state.next_turns:
        assert(turn[Turn.FRACTION] in data['fractions'])
        assert(turn[Turn.TYPE] == Turn.Type.HQ_PLACEMENT)
    
    moloch_state = state.players['moloch']
    assert(moloch_state.hand.tokens == ['klaun'])
    assert(moloch_state.hand.active_token == 0)
    assert('klaun' not in moloch_state.pile.tokens)
    assert('sztab' not in moloch_state.pile.tokens)
    assert(len(moloch_state.pile.tokens) > 0)

    borgo_state = state.players['borgo']
    assert(borgo_state.hand.tokens == [])
    assert(borgo_state.hand.active_token == None)
    assert(len(borgo_state.pile.tokens) > 0)

    assert(state.board.board[2][2].zeton_to_json() == {Token.FRACTION : "moloch", Token.NAME : "sztab", Token.ROTATION : 1, Token.DAMAGE : 0, Token.WIRED : False})