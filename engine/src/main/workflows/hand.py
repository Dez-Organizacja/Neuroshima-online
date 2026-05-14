
from main.state.contex import ActionContext
from main.steps.config import InputStepConfig, DecisionStepConfig
from main.workflows.base import Workflow
from main.state.user_action import UserAction
from main.workflows.data import WorkflowData, WorkflowName, ABILITY_WORKFLOW_REGISTRY
from main.rules.workflow.base import WorkflowRules

class HandWorkflow(Workflow):
    def __init__(self):
        super().__init__(rules=WorkflowRules())

    def build_slot_step(self):
        return InputStepConfig(
            getter = UserAction.get_slot,
            setter = WorkflowData.set_slot,
        )
            
    def build_decision_step(self):
        def decision_func(ctx : ActionContext):
            token = ctx.player.hand.get_active_token()
            ability = token.get_ability()
            return ABILITY_WORKFLOW_REGISTRY[ability]

        return DecisionStepConfig(
            decision_func=decision_func,
        )

    def build_steps(self):
        return [
            self.build_slot_step(),
            self.build_decision_step(),
        ]