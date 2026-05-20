from main.state.contex import ActionContext
from main.rules.workflow.base import WorkflowRules
from main.utils.variable import Bottom
from main.board.board_query import BoardQuery

class TurnRules(WorkflowRules):
    @staticmethod
    def can_end_turn(ctx : ActionContext):
        return not ctx.player.hand.is_full()
    
    @staticmethod
    def get_available_tokens(ctx : ActionContext):
        return {ctx.fraction : [i for i in range(ctx.state.player.hand.size)]}
    
    @staticmethod
    def get_available_bottoms(ctx : ActionContext):
        if TurnRules.can_end_turn(ctx):
            return [Bottom.END_TURN]
        else:
            return []
        
    @staticmethod
    def get_available_positions(ctx : ActionContext):
        pass