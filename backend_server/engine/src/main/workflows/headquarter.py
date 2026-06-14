from main.events.data import Event
from main.events.effects import DrawNamedTokenEffect
from main.events.flow import StartTurnEvent, EndTurnEvent
from main.state.contex import ActionContext
from main.tokens.data import BoardType
from main.workflows.base import Workflow
from main.workflows.data import WorkflowConfig, WorkflowName
from main.workflows.providers.base import WorkflowActionProvider

class HeadquarterTurnProvider(WorkflowActionProvider):
    def get_available_tokens(self, ctx: ActionContext):
        return [
            idx
            for idx, token_name in enumerate(ctx.player.hand.tokens)
            if token_name == BoardType.HQ.value
        ]

class HeadquarterTurnWorkflow(Workflow[HeadquarterTurnProvider]):
    def __init__(self, config: WorkflowConfig):
        self.config: WorkflowConfig = config
        super().__init__(action_provider=HeadquarterTurnProvider())

    def start_turn_resolve(self, ctx: ActionContext) -> list[Event]:
        return [StartTurnEvent(faction=self.config.faction)]

    @staticmethod
    def draw_token(ctx : ActionContext):
        return [DrawNamedTokenEffect(BoardType.HQ.value)]
 
    @staticmethod
    def end_turn_resolve(ctx: ActionContext) -> list[Event]:
        return [EndTurnEvent(turn_name=WorkflowName.HEADQUARTER_TURN)]

    # def finish(self, ctx : ActionContext):
    #     return self.end_turn_resolve(ctx)
    # @staticmethod
    # def clear_wf_data(ctx : ActionContext):
    #     return [ClearWorkflowDataEffect()]

    # def build_init_step(self):
    #     return ResolveStepConfig(resolve_func=self.start_turn_resolve)

    # def build_clear_step(self):
    #     return ResolveStepConfig(resolve_func=lambda ctx: [ClearWorkflowDataEffect()])

    # def build_waiting_step(self):
    #     return WaitingStepConfig()

    # def build_hand_step(self):
    #     return InitStepConfig(wf_name=WorkflowName.HAND)

    # def build_end_step(self):
    #     return ResolveStepConfig(resolve_func=self.end_turn_resolve, wf_finished=True)

    def _build_steps(self):
        return [
            self.build_resolve_step(
                self.start_turn_resolve,
                self.clear_wf_data,
            ),
            self.build_resolve_step(self.draw_token),
            self.build_input_step(message="Select your headquarters token."),
            self.build_push_workflow_step(name=WorkflowName.HAND),
            self.build_resolve_step(self.end_turn_resolve),
            # self.build_end_step()
        ]
            # self.build_init_step(),
            # self.build_clear_step(),
            # self.build_waiting_step(),
            # self.build_hand_step(),
            # self.build_end_step(),
