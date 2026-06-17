from main.workflows.data import WorkflowName, WorkflowConfig
from main.input.data import HandAction, ActionType
from main.events.workflow import PushWorkflow, GoToStep
from main.events.effects import (
    ResetAbilityUsedEffect, 
    DrawTokensEffect,
    ClearWorkflowDataEffect,
)
from main.events.flow import EndTurnEvent, StartTurnEvent
from .builder import ScenarioBuilder
from .registry import register
from main.state.context import ActionContext

name = WorkflowName.TURN
@register(name)
def turn_scenario():
    def setup_function(ctx : ActionContext):
        ctx.faction="moloch"
        for name in ("szturmowiec", "wartownik", "klaun"):
            ctx.player.hand.add(name)
        ctx.faction = ""

    return (
        ScenarioBuilder(name, config=WorkflowConfig(faction="moloch"))
        .tick()
        .given(setup_function)
        .then_execution(
            events=[
                StartTurnEvent(faction="moloch"), 
                PushWorkflow(
                    name=WorkflowName.DRAW, 
                    config=WorkflowConfig(hand_limit=3)
                )
            ],
        )

        .tick()
        .then_execution(
            events=[PushWorkflow(name=WorkflowName.ACTION)]
        )

        .tick()
        .then_execution(
            events=[GoToStep(index=1)],
            advance=False
        )
        # .when(HandAction(slot=1))
        # .then_execution(events=[ConsumeOnClick()])
        # .then_data_delta(type=ActionType.HAND, slot=1)

        # .tick()
        # .given_wf_onclick_consumed()
        # .then_execution(
        #     events=[PushWorkflow(name=WorkflowName.HAND)]
        # )


    ).build()