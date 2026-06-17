from main.workflows.base import Workflow
from main.workflows.data import WorkflowName
from main.rules.ability.movement import MoveRules
from main.state.context import ActionContext

class MovementWorkflow(Workflow):
    @staticmethod
    def check_repeat(ctx : ActionContext) -> bool:
        return MoveRules.can_execute(ctx, ctx.workflow_data.unit_pos)
        # return (
        #     MoveRules.can_use(ctx, ctx.workflow_data.unit_pos)
        #     and ctx.player.has_moves
        # )

    def _build_steps(self):
        return [
            self.build_push_workflow_step(WorkflowName.MOVE),
            self.build_repeat_step(index=0, func=self.check_repeat),
            self.build_end_step(),
        ]