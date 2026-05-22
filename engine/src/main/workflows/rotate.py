from main.workflows.base import Workflow
from main.steps.config import (
    WaitingStepConfig,
    SetStepConfig
)
from main.state.user_action import RotationAction
from main.workflows.data import WorkflowData
from main.state.contex import ActionContext
from main.events.data import ActionResult
from main.events.effects import RotateEffect
from main.workflows.providers.movement import RotateProvider
from main.workflows.step_builders import build_end_step


class RotateWorkflow(Workflow[RotateProvider]):
    def __init__(self):
        super().__init__(action_provider=RotateProvider())

    def build_waiting_step(self):
        av_config = self.action_provider.build_av_actions_config()
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

    def build_steps(self):
        return [
            self.build_waiting_step(),
            self.build_set_step(),
            build_end_step(self.resolve_function)
        ]