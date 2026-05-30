from main.workflows.data import WorkflowName, TurnConfig
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
        ctx.faction=""
        for name in ("szturmowiec", "wartownik", "klaun"):
            ctx.player.hand.add(name)

    return (
        ScenarioBuilder(name, config=TurnConfig("moloch"))
        .tick()
        .given(setup_function)
        .then_execution(
            effects=[ResetAbilityUsedEffect(positions=[]), DrawTokensEffect()],
        )

        .tick()
        .then_execution(
            effects=[ClearWorkflowDataEffect()]
        )

        .when(HandAction(slot=1))
        .then_data_delta(type=ActionType.HAND, slot=1)

        .tick()
        .then_execution(
            workflows=[PushWorkflow(name=WorkflowName.HAND)]
        )

        .tick()
        .then_execution(
            workflows=[GoToStep(index=1)],
            advance=False
        )

        .tick()
        .then_execution(
            flow_events=[EndTurnEvent()]
        )

    ).build()