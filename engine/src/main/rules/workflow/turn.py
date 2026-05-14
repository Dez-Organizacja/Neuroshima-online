from main.state.contex import ActionContext
from main.rules.workflow.base import WorkflowRules
from main.workflows.data import WorkflowName
from main.utils.variable import Bottom
from main.state.user_action import Type as ActionType

class TurnRules(WorkflowRules):
    @staticmethod
    def can_end_turn(ctx : ActionContext):
        return not ctx.player.hand.is_full()

    @staticmethod
    def get_available_sources(ctx : ActionContext):
        return []
    
    @staticmethod
    def get_available_tokens(ctx : ActionContext):
        return {ctx.fraction : [i for i in range(ctx.state.player.hand.size)]}
    
    @staticmethod
    def get_available_bottoms(ctx : ActionContext):
        if TurnRules.can_end_turn(ctx):
            return [Bottom.END_TURN]
        else:
            return []