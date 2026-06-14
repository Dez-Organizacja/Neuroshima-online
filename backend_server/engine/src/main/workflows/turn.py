from main.state.contex import ActionContext
from main.workflows.base import Workflow
from main.workflows.providers.turn import TurnProvider
from main.workflows.data import WorkflowName, WorkflowConfig
from main.events.data import Event
from main.events.flow import EndTurnEvent, StartTurnEvent
from main.rules.turn import TurnRules

class TurnWorkflow(Workflow[TurnProvider]):
    def __init__(self, config : WorkflowConfig):
        self.rules : TurnRules = TurnRules()
        self.config : WorkflowConfig = config
        super().__init__(action_provider=TurnProvider())

    def start_turn_resolve(self, ctx : ActionContext) -> list[Event]:
        return [
            StartTurnEvent(
                faction=self.config.faction,
                positions=self.rules.get_units_to_reset(ctx, self.config.faction),
            ),
        ]


    @staticmethod
    def end_turn_resolve(ctx : ActionContext) -> list[Event]:
        return [EndTurnEvent()]
    
    @staticmethod
    def dispatch(ctx : ActionContext) -> WorkflowName:
        if ctx.workflow_data.slot is not None:
            return WorkflowName.HAND
        else:
            return WorkflowName.BOARD

    def draw_tokens(self, ctx : ActionContext):
        return self.push_workflow(
            name=WorkflowName.DRAW,
            config=WorkflowConfig(hand_limit=self.config.hand_limit)
        )

    def _build_steps(self):
        return [
            self.build_resolve_step(
                self.start_turn_resolve,
                self.draw_tokens,
            ),
            self.build_resolve_step(self.clear_wf_data),
            self.build_input_step(message="Select a token or unit action."),
            self.build_dispatch_step(self.dispatch),
            self.build_repeat_step(index=1),
        ]
