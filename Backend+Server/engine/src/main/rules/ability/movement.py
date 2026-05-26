from main.rules.ability.base import AbilityRules
from main.state.contex import ActionContext
from main.board.board_query import BoardQuery
from main.rules.predicates import (
    adjacent_to,
    is_ally, 
    is_empty_at,
    is_enemy_of,
    NOT,
    is_wired_at,
)

class MoveRules(AbilityRules):
    @staticmethod
    def get_sources(ctx : ActionContext):
        candidates = BoardQuery([
            is_ally(ctx.fraction),
            NOT(is_wired_at),
        ]).apply(ctx)

        return [pos for pos in candidates 
                if any(MoveRules.get_destinations(ctx, pos))
        ]
    
    @staticmethod
    def get_destinations(ctx : ActionContext, unit_pos):
        query = BoardQuery([
            adjacent_to(unit_pos),
            is_empty_at
        ])
        return query.apply(ctx) + [unit_pos] 
    
    @staticmethod
    def get_targets(ctx : ActionContext):
        return super().get_targets(ctx)
    
    @staticmethod
    def can_use(ctx : ActionContext, pos : tuple[int, int]) -> bool:
        return not ctx.board.get_tile(pos).is_wired
    
class PushRules(AbilityRules):
    @staticmethod
    def get_destinations(ctx : ActionContext, pusher_pos, target_pos):
        return BoardQuery([
            is_empty_at,
            adjacent_to(target_pos),
            NOT(adjacent_to(pusher_pos))
        ]).apply(ctx)

    @staticmethod
    def get_targets(ctx : ActionContext, pusher_pos):
        candidates = BoardQuery([
            adjacent_to(pusher_pos),
            NOT(is_wired_at),
            is_enemy_of(ctx.board.get_tile(pusher_pos)),
        ]).apply(ctx)
        return [pos for pos in candidates
                if any(PushRules.get_destinations(ctx, pusher_pos, pos))]
    
    @staticmethod
    def get_sources(ctx):
        candidates = BoardQuery([
            is_ally(ctx.fraction),
            NOT(is_wired_at),
        ]).apply(ctx)

        return [pos for pos in candidates 
                if any(PushRules.get_targets(ctx, pos))
        ]

    @staticmethod
    def can_use(ctx : ActionContext, pos : tuple[int, int]) -> bool:
        pusher = ctx.board.get_tile(pos)
        if pusher.is_wired:
            return False
        
        return any(PushRules.get_targets(ctx, pos))