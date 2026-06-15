from main.workflows.base import Workflow
from main.workflows.data import WorkflowName
from main.workflows.providers.action import ActionProvider
from main.state.context import ActionContext
from main.events.flow import EndActionEvent

class AcitonWorkflow(Workflow[ActionProvider]):
    def __init__(self):
        super().__init__(ActionProvider())

    @staticmethod
    def dispatch(ctx : ActionContext) -> WorkflowName:
        if ctx.workflow_data.slot is not None:
            return WorkflowName.HAND
        else:
            return WorkflowName.BOARD

    @staticmethod
    def resolve(ctx : ActionContext):
        return [EndActionEvent()]

    def _build_steps(self):
        return [
            self.build_resolve_step(self.clear_wf_data),
            self.build_input_step(message="Select a token or unit action.", snapshot=True),
            self.build_dispatch_step(self.dispatch),
            self.build_end_step(self.resolve),
        ]