from main.workflows.data import WorkflowName, WorkflowConfig
from main.input.data import HandAction, ActionType
from main.events.workflow import PushWorkflow, GoToStep
from main.events.effects import (
    ResetAbilityUsedEffect, 
    DrawTokensEffect,
    ClearWorkflowDataEffect
    
)
from main.events.flow import EndTurnEvent
from .builder import ScenarioBuilder
from .registry import register
from main.state.contex import ActionContext

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
            events=[ResetAbilityUsedEffect(positions=[]), DrawTokensEffect()],
        )
        .then_faction("moloch")
        .then_faction("moloch", turn=True)

        .tick()
        .then_execution(
            events=[ClearWorkflowDataEffect()]
        )

        .when(HandAction(slot=1))
        .then_data_delta(type=ActionType.HAND, slot=1)

        .tick()
        .then_execution(
            events=[PushWorkflow(name=WorkflowName.HAND)]
        )

        .tick()
        .then_execution(
            events=[GoToStep(index=1)],
            advance=False
        )

        .tick()
        .then_execution(
            events=[EndTurnEvent()]
        )
        .then_faction("")
        .then_faction("", turn=True)

    ).build()