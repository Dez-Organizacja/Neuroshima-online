from main.state.contex import ActionContext
from main.tokens.abstract_token import Token

def NOT(predicate):
    def not_predicate(ctx : ActionContext, pos):
        return not predicate(ctx, pos)
    return not_predicate

def is_ally(fraction : str):
    def predicate(ctx : ActionContext, pos):
        token = ctx.board.get_tile(pos)
        return token.fraction == fraction
    return predicate

def is_ally_of(unit : Token):
    return is_ally(unit.fraction)

def is_enemy(fraction : str):
    def predicate(ctx : ActionContext, pos):
        token = ctx.board.get_tile(pos)
        return token.fraction != fraction
    return predicate

def is_enemy_of(unit : Token):
    return is_enemy(unit.fraction)

def is_empty_at(ctx : ActionContext, pos):
    return ctx.board.get_tile(pos) is None

def is_on_border(ctx : ActionContext, pos):
    return ctx.board.on_border(pos)

def is_wired_at(ctx : ActionContext, pos):
    return ctx.board.get_tile(pos).is_wired

def is_hq_at(ctx : ActionContext, pos):
    return ctx.board.get_tile(pos).is_hq

def adjacent_to(my_pos):
    def predicate(ctx : ActionContext, pos):
        return pos in ctx.board.adjacent_hexes(my_pos)
    return predicate

def has_ability(ctx : ActionContext, pos):
    token = ctx.board.get_tile(pos)
    return token.get_ability() is not None

def has_used_ability(ctx : ActionContext, pos):
    token = ctx.board.get_tile(pos)
    return has_ability(ctx, pos) and token.ability_used