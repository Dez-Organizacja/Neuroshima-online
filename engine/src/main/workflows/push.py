from main.state.contex import ActionContext
from main.workflows.base import Workflow
from main.rules.workflow.movement import PushRules
from main.steps.config import ResolveStepConfig
from main.events.effects import MoveEffect
from main.actions.execute.result import ActionResult
from main.workflows.step_builders import BoardSelectionMixin, build_end_step

class PushWorkflow(BoardSelectionMixin, Workflow[PushRules]):
    def __init__(self):
        super().__init__(rules=PushRules())

    def build_end_step(self):
        return ResolveStepConfig(
            resolve_func=self.resolve_push,
            wf_finished=True
        )

    def build_steps(self):
        return [
            self.build_source_step(),
            self.build_target_step(),
            self.build_destination_step(),
            build_end_step()
        ]

    @staticmethod
    def resolve_push(ctx : ActionContext):
        move = MoveEffect(
            from_pos=ctx.workflow_data.target_pos,
            to_pos=ctx.workflow_data.destination
        )
        return ActionResult(effects=[move])
    
    @classmethod
    def get_first_step_index(cls, ctx : ActionContext):
        return 2 if ctx.workflow_data.unit_pos else 0