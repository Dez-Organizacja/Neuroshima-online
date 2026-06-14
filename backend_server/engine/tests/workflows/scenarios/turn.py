from main.workflows.data import WorkflowName, WorkflowConfig
from main.input.data import HandAction, ActionType
from main.events.workflow import PushWorkflow, GoToStep, ConsumeOnClick
from main.events.effects import (
    ResetAbilityUsedEffect, 
    DrawTokensEffect,
    ClearWorkflowDataEffect,
    MaybePushUnhappyDrawEffect
)
from main.events.flow import EndTurnEvent, StartTurnEvent
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
            events=[
<<<<<<< HEAD
                ResetAbilityUsedEffect(positions=[]), 
                DrawTokensEffect(),
                MaybePushUnhappyDrawEffect(faction='moloch'),
=======
                StartTurnEvent(faction="moloch"), 
                PushWorkflow(
                    name=WorkflowName.DRAW, 
                    config=WorkflowConfig(hand_limit=3)
                )
>>>>>>> 03822f3 (działa ekspozja, medycy, sekwencja końcowa, nieszcześliwy dociąg i discard pierwszego żetou w turze)
            ],
        )

        .tick()
        .then_execution(
            events=[ClearWorkflowDataEffect()]
        )

        .when(HandAction(slot=1))
        .then_execution(events=[ConsumeOnClick()])
        .then_data_delta(type=ActionType.HAND, slot=1)

        .tick()
        .given_wf_onclick_consumed()
        .then_execution(
            events=[PushWorkflow(name=WorkflowName.HAND)]
        )

        .tick()
        .then_execution(
            events=[GoToStep(index=1)],
            advance=False
        )

    ).build()