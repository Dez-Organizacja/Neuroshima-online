from main.workflows.providers.base import WorkflowActionProvider
from main.input.data import Button
from main.state.contex import ActionContext
from main.board.board_query import BoardQuery
from main.rules.predicates import is_empty_at

class PlacementProvider(WorkflowActionProvider):
    def get_available_buttons(self, ctx : ActionContext):
        return [Button.CANCEL, Button.DISCARD]
    
    def get_available_positions(self, ctx : ActionContext):
        return BoardQuery([is_empty_at]).apply(ctx)