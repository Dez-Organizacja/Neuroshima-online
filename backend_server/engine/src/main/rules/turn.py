from main.state.context import ActionContext
from main.board.query import BoardQuery
from main.board.data import Hex
from main.rules.predicates import is_empty_at, is_ally, has_ability
from main.rules.ability.movement import MoveRules, PushRules
from main.tokens.data import Ability
from main.tokens.hand import Hand
from main.tokens.data import TokenType
from main.tokens.token_factory import TokenFactory

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

        return rules.can_use(ctx, pos) and token.can_use_ability()
    
    @staticmethod
    def end_turn_check(ctx : ActionContext) -> bool:
        return any(BoardQuery([is_empty_at]).apply(ctx.board))
    
    @staticmethod
    def get_units_to_reset(ctx : ActionContext, faction : str) -> list[Hex]:
        return BoardQuery([
            is_ally(faction),
            has_ability
        ]).apply(ctx.board)


    @staticmethod
    def can_skip_discarding_phase(ctx : ActionContext):
        return not ctx.player.hand.is_full
    
    @staticmethod
    def is_unhappy_draw(hand : Hand, faction : str):
        return all(
            TokenFactory.create(hand.get(i), faction).type == TokenType.INSTANT
            for i in range(hand.size)
        ) and hand.size