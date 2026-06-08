from main.board.query import BoardQuery
from main.events.data import Event
from main.events.effects import (
    ClearWorkflowDataEffect,
    DrawNamedTokenEffect,
)
from main.rules.predicates import is_empty_at
from main.state.contex import ActionContext
from main.steps.config import InitStepConfig, ResolveStepConfig, WaitingStepConfig
from main.tokens.data import BoardType
from main.workflows.base import Workflow
from main.workflows.data import WorkflowConfig, WorkflowName
from main.workflows.providers.base import WorkflowActionProvider
from main.workflows.step_builders import build_end_step
from main.events.flow import EndTurnEvent

class HeadquarterTurnProvider(WorkflowActionProvider):
    def get_available_tokens(self, ctx: ActionContext):
        return [
            idx
            for idx, token_name in enumerate(ctx.player.hand.tokens)
            if token_name == BoardType.HQ.value
        ]

class HeadquarterPlaceProvider(WorkflowActionProvider):
    def get_available_positions(self, ctx: ActionContext):
        return BoardQuery([is_empty_at]).apply(ctx)

class HeadquarterTurnWorkflow(Workflow[HeadquarterTurnProvider]):
    def __init__(self, config: WorkflowConfig):
        self.config: WorkflowConfig = config
        super().__init__(action_provider=HeadquarterTurnProvider())

    def start_turn_resolve(self, ctx: ActionContext) -> list[Event]:
        ctx.faction = self.config.faction
        return [DrawNamedTokenEffect(BoardType.HQ.value)]

 
    @staticmethod
    def end_turn_resolve(ctx: ActionContext) -> list[Event]:
        ctx.faction = ""
        return []

    def build_init_step(self):
        return ResolveStepConfig(resolve_func=self.start_turn_resolve)

    def build_clear_step(self):
        return ResolveStepConfig(resolve_func=lambda ctx: [ClearWorkflowDataEffect()])

    def build_waiting_step(self):
        return WaitingStepConfig()

    def build_hand_step(self):
        return InitStepConfig(wf_name=WorkflowName.HAND)

    def build_end_step(self):
        return ResolveStepConfig(resolve_func=self.end_turn_resolve, wf_finished=True)

    def _build_steps(self):
        return [
            self.build_init_step(),
            self.build_clear_step(),
            self.build_waiting_step(),
            self.build_hand_step(),
            self.build_end_step(),
        ]

# class HeadquarterPlaceWorkflow(Workflow[HeadquarterPlaceProvider]):
#     def __init__(self):
#         super().__init__(action_provider=HeadquarterPlaceProvider())

#     @staticmethod
#     def resolve_function(ctx: ActionContext) -> list[Event]:
#         slot = ctx.workflow_data.slot
#         token_name = ctx.player.hand.get(slot)

#         return [
#             PlaceEffect(
#                 pos=ctx.workflow_data.unit_pos,
#                 name=token_name,
#                 faction=ctx.faction,
#             ),
#             DiscardTokenEffect(slot),
#         ]

#     def _build_steps(self):
#         return [
#             WaitingStepConfig(
#                 action_handler=ActionHandler(
#                     setter=WorkflowData.set_unit_pos,
#                     allowed_action_types=[ActionType.BOARD],
#                     allow_buttons=False,
#                 )
#             ),
#             build_end_step(self.resolve_function),
#         ]
