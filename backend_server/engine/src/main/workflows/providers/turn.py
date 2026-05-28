from main.workflows.providers.base import WorkflowActionProvider
from main.rules.turn import TurnRules
from main.input.data import Button
from main.state.contex import ActionContext
from main.rules.predicates import (
    is_ally,
    has_ability,
    NOT,
    has_used_ability
)
from main.board.board_query import BoardQuery

class TurnProvider(WorkflowActionProvider):
    def __init__(self):
        self.rules = TurnRules()

    def get_available_buttons(self, ctx : ActionContext):
        if self.rules.can_end(ctx):
            return [Button.END_TURN]
        else:
            return []
        
    def get_available_positions(self, ctx : ActionContext):
        return BoardQuery([
            is_ally(ctx.faction),
            has_ability,
            NOT(has_used_ability)
        ]).apply(ctx)
    
    def get_available_tokens(self, ctx : ActionContext):
        return [i for i in range(ctx.player.hand.size)]