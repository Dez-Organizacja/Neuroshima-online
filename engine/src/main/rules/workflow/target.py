from main.rules.workflow.base import WorkflowRules
from abc import ABC, abstractmethod
from main.utils.variable import Bottom
from main.board.board_query import BoardQuery
import main.rules.predicates as pr
from main.state.contex import ActionContext

class TargetWorkflowRules(ABC, WorkflowRules):
    @staticmethod
    def get_available_bottoms(ctx : ActionContext):
        return [Bottom.CANCEL, Bottom.DISCARD]
    
    @abstractmethod
    @staticmethod
    def get_available_tragets(ctx : ActionContext):
        pass

    @staticmethod
    def get_available_tokens(ctx):
        return super().get_available_tokens(ctx)

class SniperRules(TargetWorkflowRules):
    @staticmethod
    def get_available_targets(ctx : ActionContext):
        query = BoardQuery([
            pr.NOT(pr.is_hq_at),
            pr.is_enemy_at
        ])
        return query.apply()

class BombRules(TargetWorkflowRules):
    @staticmethod
    def get_available_tokens(ctx : ActionContext):
        query = BoardQuery([pr.is_not_on_border])
        return query.apply()

class GrenadeRules(TargetWorkflowRules):
    @staticmethod
    def get_available_tokens(ctx : ActionContext):
        positions = []
        pos = ctx.board.get_hq_pos(ctx.fraction)
        if ctx.rules.is_hq_not_wired(ctx.fraction):
            query = BoardQuery([
                pr.adjacent_to(pos),
                pr.is_enemy_at,
                pr.NOT(pr.is_hq_at)
            ])