from main.workflows.base import Workflow
from main.steps.config import (
    WaitingStepConfig,
    ResolveStepConfig,
    SetStepConfig
)
from main.state.user_action import RotationAction
from main.workflows.data import WorkflowData
from main.state.contex import ActionContext
from main.actions.execute.result import ActionResult
from main.events.effects import RotateEffect
from main.rules.workflow.movement import RotateRules

class RotateWorkflow(Workflow[RotateRules]):
    def __init__(self):
        super().__init__(rules=RotateRules())

    def build_waiting_step(self):
        av_config = self.rules.build_av_actions_config()
        return WaitingStepConfig(av_actions_config=av_config)
    
    def build_set_step(self):
        return SetStepConfig(
            getter=RotationAction.get_rotation,
            setter=WorkflowData.set_rotation
        )
    
    @staticmethod
    def resolve_function(ctx : ActionContext):
        return ActionResult(effects=[
            RotateEffect(
                pos = ctx.workflow_data.unit_pos,
                rotation=ctx.workflow_data.rotation
            )
        ])

    def build_end_step(self):
        return ResolveStepConfig(
            resolve_func=self.resolve_function,
            wf_finished=True
        )

    def build_steps(self):
        return [
            self.build_waiting_step(),
            self.build_set_step(),
            self.build_end_step()
        ]