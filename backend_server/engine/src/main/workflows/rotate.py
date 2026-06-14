from main.workflows.base import Workflow
from main.steps.config import (
    WaitingStepConfig,
)
from main.state.contex import ActionContext
from main.events.data import Event
from main.events.effects import RotateEffect
from main.workflows.providers.movement import RotateProvider

class RotateWorkflow(Workflow[RotateProvider]):
    def __init__(self):
        super().__init__(action_provider=RotateProvider())

    # def build_waiting_step(self):
    #     return WaitingStepConfig()
    
    @staticmethod
    def resolve_function(ctx : ActionContext) -> list[Event]:
        rotate = RotateEffect(
            pos = ctx.workflow_data.unit_pos,
            rotation=ctx.workflow_data.rotation
        )
        return [rotate]

    def _build_steps(self):
        return [
            self.build_input_step(),
            self.build_resolve_step(self.resolve_function),
            self.build_end_step(),
        ]
            # self.build_waiting_step(),
            # build_end_step(self.resolve_function)
