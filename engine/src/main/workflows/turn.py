from main.state.contex import ActionContext
from main.steps.config import InitStepConfig, WaitingStepConfig
from main.workflows.base import Workflow
from main.rules.workflow.core import TurnRules
from main.state.user_action import UserAction, Type as ActionType
from main.workflows.data import WorkflowData, WorkflowName
from main.actions.available.config import AvActionsConfig

class TurnWorkflow(Workflow[TurnRules]):
    def __init__(self):
        super().__init__(rules=TurnRules())

    def build_waiting_step(self):
        pass
        # return WaitingStepConfig(
            # av_actions_config=self.
        # )

    def build_input_steps(self):
        return []

    # def build_type_step(self):
    #     return InputStepConfig(
    #         getter = UserAction.get_type,
    #         setter = WorkflowData.set_type,
    #         consume_action=False,
    #         get_positions = self.rules.get_sources,
    #         get_bottoms = self.rules.get_available_bottoms,
    #         get_available_tokens = self.rules.get_available_tokens
    #     )
    
    # def build_decision_step(self):
    #     def decision_func(ctx : ActionContext):
    #         if ctx.workflow_data.type == ActionType.HAND:
    #             return WorkflowName.HAND
    #         else:
    #             return WorkflowName.BOARD
    #     return InitStepConfig(
    #         decision_func = decision_func,
    #     )

    # def build_end_step(self):
    #     return InitStepConfig(
    #         decision_func = self.next_workflow_maker(WorkflowName.TURN),
    #         as_child = False
    #     )

    # def build_steps(self):
    #     return [
    #         self.build_type_step(),
    #         self.build_decision_step(),
    #         self.build_end_step()
    #     ]