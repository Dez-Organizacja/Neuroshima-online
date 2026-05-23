from main.actions.available.config import AvailableActionProvider
from main.state.contex import ActionContext
from main.workflows.factory import WorkflowFactory

class ProviderFactory:
    @classmethod
    def create(ctx : ActionContext) -> AvailableActionProvider:
        wf = WorkflowFactory.create(ctx.workflow_instance.config)
        step = wf.get_current_step(ctx)
        return step.get_available_actions(ctx)