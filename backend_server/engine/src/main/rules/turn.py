from main.state.contex import ActionContext
from main.board.query import BoardQuery
from main.rules.predicates import is_empty_at
from main.rules.ability.movement import MoveRules, PushRules
from main.tokens.data import Ability

ABILITY_RULES = {
    Ability.MOVE: MoveRules,
    Ability.PUSH: PushRules,
}

class TurnRules:
    @staticmethod
    def can_end(ctx : ActionContext) -> bool:
        return True

    @staticmethod
    def can_use_ability(ctx : ActionContext, pos : tuple[int, int]) -> bool:
        token = ctx.board.get_token(pos)
        rules = ABILITY_RULES.get(token.get_ability())
        if rules is None:
            return True

        return rules.can_use(ctx, pos)
    
    @staticmethod
    def end_turn_check(ctx : ActionContext) -> bool:
        return any(BoardQuery([is_empty_at]).apply(ctx.board))
