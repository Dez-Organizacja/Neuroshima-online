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

    @staticmethod
    def get_available_tokens(ctx):
        return super().get_available_tokens(ctx)

class PushRules(WorkflowRules):
    @staticmethod
    def can_be_pushed(ctx : ActionContext, pusher_pos, target_pos):
        if pr.is_wired_at(ctx, target_pos):
            return False
        if not pr.is_enemy_at(ctx, target_pos):
            return False

        candidates = BoardQuery([
            pr.is_enemy_at,
            pr.adjacent_to(target_pos),
            pr.NOT(pr.adjacent_to(pusher_pos))
        ]).apply(ctx)
        return len(candidates) >= 1
            
    @staticmethod
    def can_push(ctx, pos):
        for hex in ctx.board.adjacent_hexes(pos):
            if PushRules.can_be_pushed(ctx, pos, hex):
                return True
        return False
    
    @staticmethod
    def get_available_sources(ctx : ActionContext):
        candidates = BoardQuery([
            pr.is_ally_at,
            pr.NOT(pr.is_wired_at),
        ]).apply(ctx)
        return [pos for pos in candidates if PushRules.can_push(ctx, pos)]
    
    @staticmethod
    def get_available_targets(ctx : ActionContext):
        pusher_pos = ctx.workflow_data.unit_pos
        candidates = BoardQuery([
            pr.is_enemy_at,
            pr.adjacent_to(pusher_pos),
            pr.NOT(pr.is_wired_at)
        ]).apply(ctx)
        return [pos for pos in candidates 
                if PushRules.can_be_pushed_by(ctx, pusher_pos, pos)]

    @staticmethod
    def get_available_destinations(ctx : ActionContext):
        pusher_pos = ctx.workflow_data.unit_pos
        target_pos = ctx.workflow_data.target_pos
        return BoardQuery([
            pr.is_empty_at,
            pr.adjacent_to(target_pos),
            pr.NOT(pr.adjacent_to(pusher_pos))
        ]).apply(ctx)
    
    @staticmethod
    def get_available_bottoms(ctx : ActionContext):
        idx = ctx.workflow_instance.current_step_index
        result = []
        if idx == 0: # mozna zdiscardowac przed wybraniem swojej jednostki(zrodła)
            result = [Bottom.DISCARD]
        if idx <= 2: # mozna cancelowac przed wybraniem celu (jednostki wroga)
            #wybieranie jednostki to 2 stepy wait i set, i pytanie o bottoms bedzie kolejnym waitstepie
            result.append(Bottom.CANCEL)
        return result
    
    @staticmethod
    def get_available_tokens(ctx):
        return super().get_available_tokens(ctx)
    
class RotateRules(WorkflowRules):
    @staticmethod
    def get_available_tokens(ctx):
        return super().get_available_tokens(ctx)
    
    @staticmethod
    def get_available_bottoms(ctx):
        return super().get_available_bottoms(ctx)
    
    @staticmethod
    def get_available_positions(ctx : ActionContext):
        return [ctx.workflow_data.unit_pos]