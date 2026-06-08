from main.rules.ability.base import AbilityRules
from main.state.contex import ActionContext
from main.board.query import BoardQuery
from main.rules.predicates import (
    token_predicate,
    is_empty_at,
    is_ally_of,
    is_ally,
    NOT,
)

class HealRules(AbilityRules):
    def get_targets(self, ctx : ActionContext, healer_pos : tuple[int, int]):
        # print(f"possible getting targets for {healer_pos}")
        healer = ctx.board.get_token(healer_pos)
        heal_directions = healer.get_heal_directions()
        candidates = [
            ctx.board.go(healer_pos, direction)
            for direction in heal_directions
        ]
        # print(f"candidates {candidates}")
        possible_targets = set(
            BoardQuery([
                NOT(is_empty_at),
                is_ally_of(healer),
                token_predicate(lambda t : t.needs_heal),
            ]).apply(ctx.board)
        )
        # print(f"posible targets {possible_targets}")
        return [pos for pos in candidates if pos in possible_targets]

    def get_sources(self, ctx : ActionContext, faction : str):
        # print(f"getting heal sources for faction {faction}")
        positions = BoardQuery([
            NOT(is_empty_at),
            is_ally(faction),
            token_predicate(lambda t : not t.wired),
            token_predicate(lambda t : not t.needs_heal),
            token_predicate(lambda t : t.is_healer)
        ]).apply(ctx.board)

        # print(f"positions {positions}")        
        return [pos for pos in positions if any(self.get_targets(ctx, pos))]
