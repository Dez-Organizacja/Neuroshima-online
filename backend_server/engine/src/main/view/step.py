from main.state.contex import ActionContext
from main.actions.available.config import AvailableActionProvider

from main.view.data import StepUIState, StepViewData
from main.workflows.providers.base import WorkflowActionProvider
from main.workflows.factory import WorkflowFactory
from main.actions.available.core import AvailableActions
from typing import TypeVar

P = TypeVar("P", bound=WorkflowActionProvider)

class StepViewBuilder:
    def build_av_actions_provider(self, provider : P) -> AvailableActionProvider:
        return AvailableActionProvider(
            get_buttons=provider.get_available_buttons,
            get_tokens=provider.get_available_tokens,
            get_positions=provider.get_available_positions
        )
    
    def build_step(self, ctx : ActionContext) -> StepViewData:
        wf = WorkflowFactory.create(ctx.workflow_instance)
        wf.build_steps()
        action_provider : P = wf.action_provider
        provider = self.build_av_actions_provider(action_provider)
        ui_state = action_provider.get_ui_state(ctx)
        current_step = wf.get_current_step(ctx)
        if not ui_state.message:
            ui_state.message = current_step.config.message
        
        return StepViewData(
            available_actions = AvailableActions.get_actions(
                ctx,
                provider,
                decision_faction=ui_state.faction,
            ),
            ui_state=ui_state
        )
