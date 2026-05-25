from main.state.contex import ActionContext
from main.steps.config import (
    InitStepConfig, 
    WaitingStepConfig, 
    ResolveStepConfig,
    RepeatStepConfig
)
from main.workflows.base import Workflow
from main.workflows.providers.turn import TurnProvider
from main.workflows.data import WorkflowData, WorkflowName, TurnConfig
from main.events.data import ExecutionResult
from main.events.effects import (
    ResetAbilityUsedEffect, 
    DrawTokensEffect,
    ClearWorkflowDataEffect,
)
from main.events.flow import EndTurnEvent
from main.board.board_query import BoardQuery
from main.rules.predicates import (
    is_ally,
    has_ability
)
from main.rules.turn import TurnRules
from typing import Callable
from main.input.action_handlers import ActionHandler

class TurnWorkflow(Workflow[TurnProvider]):
    def __init__(self, config : TurnConfig):
        self.rules : TurnRules = TurnRules()
        self.config : TurnConfig = config
        self.start_turn_resolve = self.create_start_turn_function()
        super().__init__(action_provider=TurnProvider())

    def create_start_turn_function(self) -> Callable[[ActionContext], ExecutionResult]:
        def start_turn_resolve(ctx : ActionContext) -> ExecutionResult:
            ctx.state.current_fraction = self.config.fraction
            positions = BoardQuery([
                is_ally(ctx.fraction),
                has_ability
            ]).apply(ctx)
            return ExecutionResult(
                effects=[
                    ResetAbilityUsedEffect(positions),
                    DrawTokensEffect(),
                ]
            )
        return start_turn_resolve

    @staticmethod
    def end_turn_resolve(ctx : ActionContext) -> ExecutionResult:
        return ExecutionResult(flow_events=[EndTurnEvent()])

    def build_init_step(self):
        return ResolveStepConfig(resolve_func=self.start_turn_resolve)

    def build_waiting_step(self):
        return WaitingStepConfig(
            action_handler=ActionHandler(WorkflowData.set_unit_pos),
            av_actions_provider=self.action_provider
        )
    
    def build_dispatch_step(self):
        def decision_function(ctx : ActionContext) -> WorkflowName:
            if ctx.workflow_data.slot:
                return WorkflowName.HAND
            else:
                return WorkflowName.BOARD
        return InitStepConfig(decision_func=decision_function)

    def build_clear_step(self):
        def resolve_func(ctx : ActionContext):
            return ExecutionResult(effects=[ClearWorkflowDataEffect()])
        return ResolveStepConfig(resolve_func=resolve_func)

    def build_repeat_step(self):
        return RepeatStepConfig(
            repeat_from_index=1,
            check_func=self.rules.end_turn_check,
        )

    def build_end_step(self):
        return ResolveStepConfig(
            resolve_func=self.end_turn_resolve,
            wf_finished=False
            #bo endturnevent popuje workflow 
        )

    def build_steps(self):
        return [
            self.build_init_step(),
            self.build_clear_step(),
            self.build_waiting_step(),
            self.build_dispatch_step(),
            self.build_repeat_step(),
            self.build_end_step(),
        ]