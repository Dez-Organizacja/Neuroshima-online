from ..builder import ScenarioBuilder
from ..build_helpers import *
from ..data import Scenario
from ..registry import ScenarioRegistry
from main.input.data import Button, ButtonAction, HandAction

@ScenarioRegistry.register("draw1")
def draw_3_instant_tokens_scenario():
    factions=["moloch", "borgo"]
    return (
        ScenarioBuilder(factions=factions)
        .given(
            setup_turn_wf(factions[0]),
            push_workflow(name(WorkflowName.DRAW), index(1)),
            hand("moloch", draw(["bitwa", "bitwa", "bomba"])),
        )

        .when(ButtonAction(Button.NO))
        .then(workflow(index(3)))
        .available_actions(tokens(0, 1, 2))

        .when(HandAction(slot=1))
        .then(
            hand("moloch", discard(1)),
            phase(Phase.ENDGAME),
            workflow(*turn_workflow("moloch"))
        )
    )