from ..build_helpers import *
from ..builder import ScenarioBuilder
from ..data import Scenario
from ..registry import ScenarioRegistry
from main.workflows.data import WorkflowName
from main.input.data import HandAction, Button, ButtonAction
from typing import Callable

def build_battle_scenario(
        factions : list[str],
        setup_board : list[Callable],
        expected_board : list[Callable],
) -> Scenario:
    
    return (
        ScenarioBuilder(factions)
        .given(
            setup_turn(factions),
            hand_add(faction=factions[0], cards=["bitwa"]),
            *setup_board,
        )

        .when(HandAction(slot=0))
        .then(
            pushing_hand_wf_changes(slot=0),
            stack_add(name=WorkflowName.START_BATTLE, index=0)
        )

        .when(ButtonAction(Button.USE))
        .then(
            *expected_board,
            # stan stacka przed start battle, hand, turn, game
            stack_pop(count=3), # pop start battle, hand, turn
            # oczekiwany stan stacku: game
            stack_index_change(index=6), 
            stack_add_turn_wf(factions[1]),
            faction_delta(factions[1], turn=True),
            wf_data_clear(),
        )
        .build()
    )
@ScenarioRegistry.register("battle1")
def pure_battle() -> Scenario:
    factions = ["moloch", "borgo"]
    setup_board = [
        tile_place(pos=(1, 3), name="lowca", faction="moloch", rotation=1),
        tile_place(pos=(1, 5), name="mutek", faction="borgo"),
        tile_place(pos=(2, 2), name="sztab", faction="moloch"),
        tile_place(pos=(2, 4), name="sztab", faction="borgo"),
    ]
    expected_board = [
        tiles_remove([(1, 3), (1, 5)]),
        tile_damage(pos=(2, 4)),
    ]
    return build_battle_scenario(factions, setup_board, expected_board)

@ScenarioRegistry.register("battle2")
def melee_initiative_boosts_and_sieciarze() -> Scenario:
    factions = ["moloch", "borgo"]
    setup_board = [
        faction_tiles_place(
            faction="borgo",
            positions=[(0, 2), (1, 5), (3, 5), (4, 4), (4, 6)],
            names=["zwiadowca", "sieciarz", "mutek", "oficer", "zwiadowca"],
            rotations=[0, 2, 0, 0, 0]
        ),
        faction_tiles_place(
            faction="moloch",
            positions=[(1, 3), (2, 4)],
            names=["sztab", "klaun"],
            rotations=[0, 0]
        ),
    ]
    expected_board = [
        tiles_remove([(2, 4)]),
        tile_damage(pos=(1, 3), damage=3),
    ]
    return build_battle_scenario(factions, setup_board, expected_board)

# tile_place(pos=(2, 6), name="zabojca", faction="borgo", rotation=5),
# tile_place(pos=(3, 3), name="mutek", faction="borgo"),
# tile_place(pos=(3, 5), name="klaun", faction="moloch"),
# tile_place(pos=(4, 4), name="zawiadowca", faction="moloch"),