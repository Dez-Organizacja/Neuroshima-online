from main.state.contex import ActionContext
from main.steps.config import (
    InitStepConfig, 
    SetStepConfig,
    WaitingStepConfig, 
    ResolveStepConfig,
    EndTurnCheckConfig,
)
from main.workflows.base import Workflow
from main.workflows.providers.turn import TurnProvider
from main.state.user_action import UserAction, Type as ActionType
from main.workflows.data import WorkflowData, WorkflowName
from main.events.data import ActionResult
from main.events.effects import (
    ResetAbilityUsedEffect, 
    DrawTokensEffect,
    ClearWorkflowDataEffect,
)
from main.board.board_query import BoardQuery
from main.rules.predicates import (
    is_ally,
    has_ability
)
from main.rules.turn import TurnRules
from main.state.user_action import UserAction
from main.workflows.data import WorkflowData

class TurnWorkflow(Workflow[TurnProvider]):
    def __init__(self):
        super().__init__(action_provider=TurnProvider())
        self.rules = TurnRules()

    @staticmethod
    def begin_turn_resolve(ctx : ActionContext) -> ActionResult:
        ctx.fraction = ctx.workflow_instance.fraction
        positions = BoardQuery([
            is_ally(ctx.fraction),
            has_ability
        ]).apply(ctx)
        return ActionResult(
            effects=[
                ResetAbilityUsedEffect(positions),
                DrawTokensEffect(),
            ]
        )

    @staticmethod
    def end_turn_resolve(ctx : ActionContext) -> ActionResult:
        ctx.fraction = ""

    def build_init_step(self):
        return ResolveStepConfig(resolve_func=self.begin_turn_resolve)

    def build_waiting_step(self):
        return WaitingStepConfig(
            av_actions_config=self.action_provider.build_av_actions_config(),
            consume_action=True
        )
    
    def build_set_step(self):
        return SetStepConfig(
            getter=UserAction.get_type,
            setter=WorkflowData.set_type
        )
    
    def build_dispatch_step(self):
        def decision_function(ctx : ActionContext) -> WorkflowName:
            if ctx.workflow_data.type == ActionType.HAND:
                return WorkflowName.HAND
            else:
                return WorkflowName.BOARD
        return InitStepConfig(decision_func=decision_function)

    def build_clear_step(self):
        def resolve_func(ctx : ActionContext):
            return ActionResult(effects=[ClearWorkflowDataEffect()])
        return ResolveStepConfig(resolve_func=resolve_func)

    def build_check_end_turn_step(self):
        return EndTurnCheckConfig(
            repeat_from_index=1,
            check_func=self.rules.end_turn_check,
            resolve_func=self.end_turn_resolve,
        )

    def build_input_steps(self):
        return [
            self.build_init_step(),
            self.build_clear_step(),
            self.build_waiting_step(),
            self.build_set_step(),
            self.build_dispatch_step(),
            self.build_check_end_turn_step()
        ]