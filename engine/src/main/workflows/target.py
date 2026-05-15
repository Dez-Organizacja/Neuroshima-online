from abc import ABC, abstractmethod
from main.workflows.base import Workflow
from main.rules.workflow.target import TargetWorkflowRules
from main.state.contex import ActionContext
from main.steps.config import InputStepConfig, ResolveStepConfig
from main.state.user_action import BoardAction
from main.workflows.data import WorkflowData
from main.actions.exeute_actions.action_result import ActionResult
from main.effects.board_effects import(
    DamageEffect, 
    DamageProfile, 
    DestroyEffect
)
from main.board.board_query import BoardQuery
import main.rules.predicates as pr

class TargetWorkflow(Workflow[TargetWorkflowRules], ABC):
    def __init__(self, rules : TargetWorkflowRules):
        super().__init__(rules)

    @abstractmethod
    @staticmethod
    def resolve_func(ctx : ActionContext) -> ActionResult:
        pass

    def build_target_step(self):
        return InputStepConfig(
            getter = BoardAction.get_pos,
            setter = WorkflowData.set_target_pos,
            get_positions = self.rules.get_available_tokens,
            get_bottoms = self.rules.get_available_bottoms
        )


    def build_end_step(self):
        return ResolveStepConfig(
            resolve_func = self.resolve_func,
            wf_finished=True
        )

    def build_steps(self):
        return [
            self.build_target_step(),
            self.build_end_step()
        ]
    
class SniperWorkflow(TargetWorkflow):
    @staticmethod
    def resolve_func(ctx : ActionContext):
        profile = DamageProfile(
            can_hit_hq=False,
            ignore_armor=True
        )
        return ActionResult(
            effects=[
                DamageEffect(
                    pos = ctx.workflow_data.target_pos,
                    profile=profile,
                    power=1
                )
            ]
        )
    
class GranadeWorkflow(TargetWorkflow):
    @staticmethod
    def resolve_func(ctx : ActionContext):
        return ActionResult(
            effects=[DestroyEffect(ctx.workflow_data.target_pos)]
        )
    
class BombWorkflow(TargetWorkflow):
    @staticmethod
    def resolve_func(ctx : ActionContext):
        pos = ctx.workflow_data.target_pos
        query = BoardQuery([
            pr.adjacent_to(pos),
            pr.NOT(pr.is_empty_at),
        ])
        positions = query.apply()
        if not pr.is_empty_at(ctx, pos):
            positions.append(pos)

        profile = DamageProfile(
            can_hit_hq=False,
            ignore_armor=True
        )
        return ActionResult(
            effects=[
                DamageEffect(pos=pos, power=1, profile=profile)
                for pos in positions       
            ]
        )