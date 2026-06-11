from main.state.contex import ActionContext
from main.workflows.data import WorkflowName
from main.events.workflow import GoToStep, DeleteAbove
from main.events.effects import ClearWorkflowDataEffect
from main.events.history import RestoreUndoSnapshotEffect

class UndoSystem:
    @staticmethod
    def before_action(ctx : ActionContext, starts_action : bool = False):
        if starts_action:
            ctx.state.create_undo_snapshot(
                workflow_name=ctx.workflow_instance.name,
                owner_faction=ctx.decision_faction,
            )

    @staticmethod
    def resolve(ctx : ActionContext):
        if not ctx.state.can_undo(ctx.decision_faction):
            if ctx.workflow_instance.name in {
                WorkflowName.TURN,
                WorkflowName.HEADQUARTER_TURN,
            }:
                return [GoToStep(ctx.workflow_instance.current_step_index)]

            return [
                DeleteAbove(name=WorkflowName.TURN),
                ClearWorkflowDataEffect()
            ]

        return [
            RestoreUndoSnapshotEffect(ctx.decision_faction)
        ]