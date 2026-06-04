from main.state.contex import ActionContext
from main.steps.config import (
    InitStepConfig, 
    WaitingStepConfig, 
    ResolveStepConfig,
    RepeatStepConfig
)
from main.workflows.base import Workflow
from main.workflows.providers.turn import TurnProvider
from main.workflows.data import WorkflowData, WorkflowName, WorkflowConfig
from main.events.data import Event
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
    def __init__(self, config : WorkflowConfig):
        self.rules : TurnRules = TurnRules()
        self.config : WorkflowConfig = config
        super().__init__(action_provider=TurnProvider())

    def start_turn_resolve(self, ctx : ActionContext) -> list[Event]:
        ctx.faction = self.config.faction
        positions = BoardQuery([
            is_ally(ctx.faction),
            has_ability
        ]).apply(ctx)
        return [
                ResetAbilityUsedEffect(positions),
                DrawTokensEffect(hand_limit=self.config.hand_limit),
            ]
    
    @staticmethod
    def end_turn_resolve(ctx : ActionContext) -> list[Event]:
        ctx.faction = ""
        return [EndTurnEvent()]

    def build_init_step(self):
        return ResolveStepConfig(resolve_func=self.start_turn_resolve)

    def build_waiting_step(self):
        return WaitingStepConfig(
            action_handler=ActionHandler(WorkflowData.set_unit_pos),
        )
    
    def build_dispatch_step(self):
        def decision_function(ctx : ActionContext) -> WorkflowName:
            # print("turn dispatch function")
            # print(f"workflow data {ctx.workflow_data}")
            if ctx.workflow_data.slot is not None:
                return WorkflowName.HAND
            else:
                return WorkflowName.BOARD
        return InitStepConfig(decision_func=decision_function)

    def build_clear_step(self):
        def resolve_func(ctx : ActionContext) -> list[Event]:
            return [ClearWorkflowDataEffect()]
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

    def _build_steps(self):
        return [
            self.build_init_step(),
            self.build_clear_step(),
            self.build_waiting_step(),
            self.build_dispatch_step(),
            self.build_repeat_step(),
            self.build_end_step(),
        ]
