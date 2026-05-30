from main.rules.ability.base import AbilityRules
from main.state.contex import ActionContext
from main.board.board_query import BoardQuery
from main.rules.predicates import (
    token_predicate,
    is_empty_at,
    NOT
)
from main.tokens.board_token import BoardToken

class HealRules(AbilityRules):
    @staticmethod
    def get_destinations(ctx, healer_pos : tuple[int, int]):
        return BoardQuery(
            [token_predicate(BoardToken.needs_heal)]
        ).apply(ctx)

    @staticmethod
    def can_heal(ctx : ActionContext, pos : tuple[int, int]) -> bool:
        token = ctx.board.get_token(pos)
        return (
            not token.is_wired()
            and not token.needs_heal
            and token.is_healer
            and any(HealRules.get_destinations(ctx, pos))
        )

    @staticmethod
    def get_sources(ctx : ActionContext):
        positions = BoardQuery([
            NOT(is_empty_at),
            NOT(token_predicate(BoardToken.is_wired)),
            NOT(token_predicate(BoardToken.needs_heal))
        ]).apply(ctx)
