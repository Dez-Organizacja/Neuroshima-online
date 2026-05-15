from abc import ABC, abstractmethod
from typing import Callable
from main.actions.data import ActionType
from main.effects.board_effects import DiscardActiveTokenEffect
from main.workflows.base import Workflow
from main.rules.workflow.base import WorkflowRules
from main.steps.config import InputStepConfig, InitStepConfig, ResolveStepConfig
from main.state.user_action import BoardAction, HandAction
from main.state.contex import ActionContext
from main.workflows.data import WorkflowData, WorkflowName
from main.actions.exeute_actions.action_result import ActionResult

class DispatchWorkflow(ABC, Workflow):
    def __init__(self, 
                 rules : WorkflowRules, 
                 decision_func : Callable[[ActionContext], WorkflowName] = None,
                 resolve_func : Callable[[ActionContext], ActionResult] = None,
        ):
        super().__init__(rules)
        self.decision_func = decision_func
        self.resolve_func = resolve_func

    @staticmethod
    def token_ability_dispatch(ctx : ActionContext):
        token = Workflow.get_active_token(ctx)
        ability = token.get_ability()
        return Workflow.get_workflow_for_ability(ability)
    
    @staticmethod
    def action_type_dispatch(ctx : ActionContext):
        if ctx.workflow_data.type == ActionType.HAND:
            return WorkflowName.HAND
        else:
            return WorkflowName.BOARD

    @abstractmethod
    def build_input_step(self):
        pass
        
    def build_decision_step(self):
        return InitStepConfig(
            decision_func=self.decision_func,
        )

    def build_end_step(self):
        return ResolveStepConfig(
            resolve_func = self.resolve_func,
            wf_finished = True
        )

    def build_steps(self):
        return [
            self.build_input_step(),
            self.build_decision_step(),
            self.build_end_step()
        ]

class HandWorkflow(DispatchWorkflow):
    def __init__(self):
        super().__init__(
            rules=WorkflowRules(),
            decision_func = self.token_ability_dispatch,
            resolve_func = self.resolve_discard,
            )

    @staticmethod
    def resolve_discard(ctx : ActionContext):
        return ActionResult(
            effects=[DiscardActiveTokenEffect()]
        )

    def build_input_step(self):
        return InputStepConfig(
            getter = HandAction.get_slot,
            setter = WorkflowData.set_slot,
        )
    
class BoardWorkflow(DispatchWorkflow):
    def __init__(self):
        super().__init__(
            rules=WorkflowRules(),
            decision_func = self.token_ability_dispatch,
        )

    def build_input_step(self):
        return InputStepConfig(
            getter = BoardAction.get_pos,
            setter = WorkflowData.set_unit_pos,
        )