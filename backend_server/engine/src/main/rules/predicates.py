from main.board.board import Board
from main.tokens.board_token import BoardToken
from main.tokens.data import Ability
from typing import Callable
from main.board.board import Hex

predicate_func = Callable[[Board, Hex], bool]

def NOT(predicate):
    def not_predicate(board : Board, pos : Hex):
        return not predicate(board, pos)
    return not_predicate

def is_ally(faction : str):
    def predicate(board : Board, pos : Hex):
        token = board.get_token(pos)
        return token is not None and token.faction == faction
    return predicate

def is_ally_of(unit : BoardToken):
    return is_ally(unit.faction)

def is_enemy(faction : str):
    def predicate(board : Board, pos : Hex):
        token = board.get_token(pos)
        return token is not None and token.faction != faction
    return predicate

def is_enemy_of(unit : BoardToken):
    return is_enemy(unit.faction)

def is_empty_at(board : Board, pos : Hex):
    return board.get_token(pos) is None

def is_on_border(board : Board, pos : Hex):
    return board.on_border(pos)

def token_predicate(func : Callable[[BoardToken], bool]):
    def predicate(board : Board, pos : Hex):
        return func(board.get_token(pos))
    return predicate

def adjacent_to(my_pos):
    def predicate(board : Board, pos : Hex):
        return pos in board.adjacent_hexes(my_pos)
    return predicate

def in_line_to(my_pos : Hex, direction : int):
    def predicate(board : Board, pos : Hex):
        return pos in board.get_line(my_pos, direction)
    return predicate

def has_ability(board : Board, pos : Hex):
    token = board.get_token(pos)
    return token.get_ability() is not None

def has_used_ability(board : Board, pos : Hex):
    token = board.get_token(pos)
    return has_ability(board, pos) and token.ability_used
