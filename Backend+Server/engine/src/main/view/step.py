from main.state.contex import ActionContext
from main.actions.available.config import AvailableActionProvider

from main.view.data import StepUIState, StepViewData
from main.workflows.providers.base import WorkflowActionProvider
from main.workflows.factory import WorkflowFactory
from main.actions.available.core import AvailableActions

class StepViewBuilder:
    def build_av_actions_provider(self, 
                                provider : WorkflowActionProvider
        ) -> AvailableActionProvider:
        
        return AvailableActionProvider(
            get_buttons=provider.get_available_buttons,
            get_tokens=provider.get_available_tokens,
            get_positions=provider.get_available_positions
        )
    
    def build_step(self, ctx : ActionContext) -> StepViewData:
        wf = WorkflowFactory.create(ctx.workflow_instance)
        action_provider : WorkflowActionProvider = wf.action_provider
        provider = self.build_av_actions_provider(action_provider)
        
        return StepViewData(
            available_actions= AvailableActions(provider).get_actions(ctx),
            ui_state= action_provider.get_ui_state(ctx)
        )