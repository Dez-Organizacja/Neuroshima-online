import pytest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from akcje import Actions
from main import Game

width = 5
length = 9
default_game_state = {'faza': 'tura', 'state': 'no_selection', 'selected': None, 'current_frakcja': 'moloch', 
                      'next_turns': [{'frakcja': 'moloch', 'typ': 'tura'}, {'frakcja': 'borgo', 'typ': 'tura'}], 
                      'board': [[None for _ in range(length)] for _ in range(width)], 
                      'pile': {"moloch" : [], 'borgo': []}, 
                      'hand': {'moloch': [], 'borgo': []}, 
                      'available_actions': {
                          'hand': {'moloch': [False, False, False], 'borgo': [False, False, False]}, 
                          'board': [[False for _ in range(length)] for _ in range(width)], 
                          'bottoms': {
                              'end_turn': False, 
                              'discard': False, 
                              'use': False, 
                              'cancel': False, 
                              'yes': False, 
                              'no': False}
                              }
                    }

# def test_zeton_bitwa():
#     data = default_game_state
#     data["hand"]["moloch"].append("bitwa")
#     data["action"] = {"type" : "hand", "slot" : 0}
#     game = Game(data)
