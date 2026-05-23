from main.workflows.base import Workflow
from main.steps.config import (
    WaitingStepConfig,
)
from main.input.data import RotationAction
from main.workflows.data import WorkflowData
from main.state.contex import ActionContext
from main.events.data import ExecutionResult
from main.events.effects import RotateEffect
from main.workflows.providers.movement import RotateProvider
from main.workflows.step_builders import build_end_step
from main.input.action_handlers import ActionHandler

class RotateWorkflow(Workflow[RotateProvider]):
    def __init__(self):
        super().__init__(action_provider=RotateProvider())

    def build_waiting_step(self):
        return WaitingStepConfig(
            action_handler=ActionHandler(),
        )
    
    @staticmethod
    def resolve_function(ctx : ActionContext):
        return ExecutionResult(effects=[
            RotateEffect(
                pos = ctx.workflow_data.unit_pos,
                rotation=ctx.workflow_data.rotation
            )
        ])

    def build_steps(self):
        return [
            self.build_waiting_step(),
            build_end_step(self.resolve_function)
        ]