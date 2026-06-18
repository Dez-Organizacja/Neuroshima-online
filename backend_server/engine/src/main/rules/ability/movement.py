from main.state.context import ActionContext
from main.board.query import BoardQuery
from main.board.data import Hex
from main.tokens.data import Ability
from main.rules.ability.base import AbilityRules
from main.rules.predicates import (
    adjacent_to,
    is_ally, 
    is_empty_at,
    is_enemy_of,
    NOT,
    token_predicate
)

class MoveRules(AbilityRules):
    ABILITY = Ability.MOVE
    @staticmethod
    def get_sources(ctx : ActionContext):
        candidates = BoardQuery([
            is_ally(ctx.faction),
            NOT(token_predicate(lambda t: t.wired)),
        ]).apply(ctx.board)

        return [pos for pos in candidates 
                if any(MoveRules.get_destinations(ctx, pos))
        ]
    
    @staticmethod
    def get_destinations(ctx : ActionContext, unit_pos : Hex):
        # print("get destinations")
        query = BoardQuery([
            adjacent_to(unit_pos),
            is_empty_at
        ])
        return query.apply(ctx.board) + [unit_pos] 
    
    # @staticmethod
    # def can_use(ctx : ActionContext, pos : Hex) -> bool:
    #     token = ctx.board.get_token(pos)
    #     return token.get_ability() == Ability.MOVE

    @staticmethod
    def can_execute(ctx : ActionContext, pos : Hex) -> bool:
        token = ctx.board.get_token(pos)
        # print("")
        return (
            not token.wired
            and len(MoveRules.get_sources(ctx)) > 0
            and ctx.state.players[token.faction].has_moves
        )
    
class PushRules(AbilityRules):
    ABILITY = Ability.PUSH
    @staticmethod
    def get_destinations(ctx : ActionContext, pusher_pos, target_pos):
        return BoardQuery([
            is_empty_at,
            adjacent_to(target_pos),
            NOT(adjacent_to(pusher_pos))
        ]).apply(ctx.board)

    @staticmethod
    def get_targets(ctx : ActionContext, pusher_pos):
        candidates = BoardQuery([
            is_enemy_of(ctx.board.get_token(pusher_pos)),
            adjacent_to(pusher_pos),
            NOT(token_predicate(lambda t : t.wired)),
        ]).apply(ctx.board)
        return [pos for pos in candidates
                if any(PushRules.get_destinations(ctx, pusher_pos, pos))]
    
    @staticmethod
    def get_sources(ctx):
        candidates = BoardQuery([
            is_ally(ctx.faction),
            NOT(token_predicate(lambda t : t.wired)),
        ]).apply(ctx.board)

        return [pos for pos in candidates 
                if any(PushRules.get_targets(ctx, pos))
        ]

    @staticmethod
    def can_execute(ctx : ActionContext, pos : Hex) -> bool:
        pusher = ctx.board.get_token(pos)
        return (
            not pusher.wired
            and len(PushRules.get_targets(ctx, pos)) > 0
        )
        # if pusher.wired:
        #     return False
        
        # return any(PushRules.get_targets(ctx, pos))
