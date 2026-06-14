from ..builder import ScenarioBuilder
from ..build_helpers import *
from ..data import Scenario
from ..registry import ScenarioRegistry
from main.input.data import BoardAction, Button

@ScenarioRegistry.register("bomb")
def bomb_scenario() -> Scenario:
    factions = ["moloch", "borgo"]
    return (
        ScenarioBuilder(factions=factions)
        .given(
            build_from_hand_action_wfs(factions),
            hand("moloch", draw(["bomba"])),
            board(
                faction_place(
                    "moloch",
                    tile((2, 0), "sztab"),
                    tile((1, 1), "klaun"),
                    tile((1, 3), "cyborg"),
                ),
                faction_place(
                    "borgo",
                    tile((2, 2), "sieciarz"),
                    tile((2, 4), "sztab"),
                )
            )
        )
        .when(BoardAction(pos=(2, 2)))
        .then(
            board(
                tiles_remove([(1, 3), (2, 2)]),
                unit((1, 1), damage()),
            ),
            hand("moloch", discard(0)),
            workflow(*turn_workflow("moloch")),
        )
        .available_actions(
            buttons(Button.END_TURN),
        )
        .build()
    )