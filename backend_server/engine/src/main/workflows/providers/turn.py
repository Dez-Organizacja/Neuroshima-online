from main.workflows.providers.base import WorkflowActionProvider
from main.rules.turn import TurnRules
from main.input.data import Button
from main.state.contex import ActionContext
from main.rules.predicates import (
    is_ally,
    has_ability,
    NOT,
    has_used_ability,
    token_predicate,
)
from main.tokens.board_token import BoardToken
from main.board.query import BoardQuery

class TurnProvider(WorkflowActionProvider):
    def __init__(self):
        self.rules = TurnRules()

    def get_available_buttons(self, ctx : ActionContext):
        if self.rules.can_end(ctx):
            return [Button.END_TURN]
        else:
            return []
        
    def get_available_positions(self, ctx : ActionContext):
        candidates = BoardQuery([
            is_ally(ctx.faction),
            has_ability,
            NOT(has_used_ability),
            NOT(token_predicate(lambda t : t.wired))
        ]).apply(ctx.board)

        return [
            pos for pos in candidates
            if self.rules.can_use_ability(ctx, pos)
        ]
    
    def get_available_tokens(self, ctx : ActionContext):
        return [i for i in range(ctx.player.hand.size)]
