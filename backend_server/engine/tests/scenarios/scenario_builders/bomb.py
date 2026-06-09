from ..builder import ScenarioBuilder
from ..delta_ops import *
from ..data import Scenario
from ..registry import ScenarioRegistry
from main.workflows.data import WorkflowName
from main.input.data import HandAction, BoardAction

@ScenarioRegistry.register("bomb")
def bomb_scenario() -> Scenario:
    factions = ["moloch", "borgo"]
    return (
        ScenarioBuilder(factions=factions)
        .given(
            setup_turn(factions),
            hand_add(faction="moloch", cards=["bomba"]),
            tile_place(pos=(2, 0), name="sztab", faction="moloch"),
            tile_place(pos=(2, 2), name="sieciarz", faction="borgo"),
            tile_place(pos=(2, 4), name="sztab", faction="borgo"),
            tile_place(pos=(1, 1), name="klaun", faction="moloch"),
            tile_place(pos=(1, 3), name="cyborg", faction="moloch"),
        )
        .when(HandAction(slot=0))
        .then(
            pushing_hand_wf_changes(slot=0),
            stack_add(name=WorkflowName.BOMB, index=0),
        )

        .when(BoardAction(pos=(2, 2)))
        .then(
            tiles_remove(positions=[(1, 3), (2, 2)]),
            tile_damage(pos=(1, 1)),
            stack_pop(), #pop hand wf
            stack_pop(), # pop bomb wf
            wf_data_clear(),
            stack_index_change(index=2),
        )
        .build()
    )