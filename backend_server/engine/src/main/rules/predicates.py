from main.state.contex import ActionContext
from main.tokens.abstract_token import Token
from typing import Callable

def NOT(predicate):
    def not_predicate(ctx : ActionContext, pos):
        return not predicate(ctx, pos)
    return not_predicate

def is_ally(faction : str):
    def predicate(ctx : ActionContext, pos):
        token = ctx.board.get_token(pos)
        return token is not None and token.faction == faction
    return predicate

def is_ally_of(unit : Token):
    return is_ally(unit.faction)

def is_enemy(faction : str):
    def predicate(ctx : ActionContext, pos):
        token = ctx.board.get_token(pos)
        return token is not None and token.faction != faction
    return predicate

def is_enemy_of(unit : Token):
    return is_enemy(unit.faction)

def is_empty_at(ctx : ActionContext, pos):
    return ctx.board.get_token(pos) is None

def is_on_border(ctx : ActionContext, pos):
    return ctx.board.on_border(pos)

def token_predicate(func : Callable[[Token], bool]):
    def predicate(ctx : ActionContext, pos):
        return func(ctx.board.get_token(pos))
    return predicate

def adjacent_to(my_pos):
    def predicate(ctx : ActionContext, pos):
        return pos in ctx.board.adjacent_hexes(my_pos)
    return predicate

def has_ability(ctx : ActionContext, pos):
    token = ctx.board.get_token(pos)
    return token.get_ability() is not None

def has_used_ability(ctx : ActionContext, pos):
    token = ctx.board.get_token(pos)
    return has_ability(ctx, pos) and token.ability_used