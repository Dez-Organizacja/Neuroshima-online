from main.workflows.providers.base import WorkflowActionProvider
from main.utils.variable import Bottom
from main.state.contex import ActionContext
from main.board.board_query import BoardQuery
from main.rules.predicates import is_empty_at

class PlacementProvider(WorkflowActionProvider):
    def get_available_bottoms(self, ctx : ActionContext):
        return [Bottom.CANCEL, Bottom.DISCARD]
    
    def get_available_positions(self, ctx : ActionContext):
        return BoardQuery([is_empty_at]).apply(ctx)