from main.rules.workflow.base import WorkflowRules
from main.utils.variable import Bottom
from main.state.contex import ActionContext
from main.board.board_query import BoardQuery
from main.rules.predicates import is_empty_at

class PlaceRules(WorkflowRules):
    @staticmethod
    def get_available_bottoms(ctx):
        return [Bottom.CANCEL, Bottom.DISCARD]
    
    @staticmethod
    def get_available_tokens(ctx):
        return super().get_available_tokens(ctx)
    
    @staticmethod
    def get_available_positions(ctx : ActionContext):
        return BoardQuery([is_empty_at]).apply()