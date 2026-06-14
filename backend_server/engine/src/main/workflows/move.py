from main.events.effects import MoveEffect
from main.state.contex import ActionContext
from main.workflows.base import Workflow
from main.workflows.data import WorkflowName
from main.workflows.providers.movement import MoveProvider
from main.workflows.step_builders import BoardSelectionMixin

class MoveWorkflow(BoardSelectionMixin, Workflow[MoveProvider]):
    def __init__(self):
        super().__init__(action_provider=MoveProvider())

    # def build_move_step(self):
    #     return ResolveStepConfig(resolve_func=self.resolve_move)

    # def build_rotate_step(self):
    #     return InitStepConfig(wf_name=WorkflowName.ROTATE)

    def _build_steps(self):
        return [
            self.build_source_step(message="Select the unit to move."),
            self.build_destination_step(message="Select the movement destination."),
            self.build_resolve_step(self.resolve_move),
            self.build_push_workflow_step(WorkflowName.ROTATE),
            self.build_end_step()
        ]
            # self.build_source_step(),
            # self.build_destination_step(),
            # self.build_move_step(),
            # self.build_rotate_step(),
            # build_end_step(),

    @staticmethod
    def resolve_move(ctx : ActionContext):
        move = MoveEffect(
            from_pos=ctx.workflow_data.unit_pos,
            to_pos=ctx.workflow_data.destination
        )
        return [move]

    @classmethod
    def get_first_step_index(cls, ctx : ActionContext):
        return 1 if ctx.workflow_data.unit_pos else 0
