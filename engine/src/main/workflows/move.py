from main.events.data import ActionResult
from main.events.effects import MoveEffect
from main.state.contex import ActionContext
from main.workflows.base import Workflow
from main.workflows.data import WorkflowName
from main.workflows.providers.movement import MoveProvider
from main.steps.config import ResolveStepConfig, InitStepConfig
from main.workflows.step_builders import BoardSelectionMixin, build_end_step

class MoveWorkflow(BoardSelectionMixin[MoveProvider], Workflow[MoveProvider]):
    def __init__(self):
        super().__init__(action_provider=MoveProvider())
        self.name = WorkflowName.MOVE
        self.get_bottoms = self.action_provider.get_available_bottoms

    def build_move_step(self):
        return ResolveStepConfig(resolve_func=self.resolve_move)

    def build_rotate_step(self):
        return InitStepConfig(wf_name=WorkflowName.ROTATE)

    def build_steps(self):
        return [
            self.build_source_steps(),
            self.build_destination_steps(),
            self.build_move_step(),
            self.build_rotate_step(),
            build_end_step(self.resolve_move),
        ]

    @staticmethod
    def resolve_move(ctx : ActionContext):
        move = MoveEffect(
            from_pos=ctx.workflow_data.unit_pos,
            to_pos=ctx.workflow_data.destination
        )
        return ActionResult(effects=[move])

    @classmethod
    def get_first_step_index(cls, ctx : ActionContext):
        return 2 if ctx.workflow_data.unit_pos else 0