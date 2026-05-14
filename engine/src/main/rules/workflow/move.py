import main.rules.predicates as pr
from main.state.contex import ActionContext
from main.board.board_query import BoardQuery
from main.utils.variable import Bottom
from main.rules.workflow.base import WorkflowRules


class MoveRules(WorkflowRules):
    @staticmethod
    def can_move(ctx : ActionContext, pos):
        for hex in ctx.board.adjacent_hexes(pos):
            if pr.is_empty_at(ctx, hex):
                return True
        return False
    
    @staticmethod
    def get_available_sources(ctx : ActionContext):
        candiates = BoardQuery([
            pr.is_ally_at,
            pr.NOT(pr.is_wired_at)
        ]).apply(ctx)
        return [p for p in candiates if MoveRules.can_move(ctx, p)]


    @staticmethod
    def get_available_destinations(ctx : ActionContext, unit_pos):
        result = BoardQuery([
            pr.is_empty_at,
            pr.adjacent_to(unit_pos)
        ]).apply(ctx)
        return result + [unit_pos]
    
    @staticmethod
    def get_available_bottoms(ctx : ActionContext):
        idx = ctx.workflow_instance.current_step_index
        result = []
        if idx == 0: # odzrucanie przed wybraniem jednostki
            result = [Bottom.DISCARD]
        if idx <= 1: # cancel przed wybraniem celu
            result.append(Bottom.CANCEL)
        return result
