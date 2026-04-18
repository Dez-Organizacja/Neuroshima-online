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