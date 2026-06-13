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
            stack_add(
                name=WorkflowName.START_BATTLE, 
                index=0, 
                config=action_workflow_config(slot=0)
            )
        )

        .when(ButtonAction(Button.USE))
        .then(
            *expected_board,
            hand_remove(faction=factions[0], index=0),
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


@ScenarioRegistry.register("battle3")
def sieciarz_blocks_attack() -> Scenario:
    factions = ["borgo", "moloch"]
    setup_board = [
        tile_place(pos=(4, 6), name="sztab", faction="borgo"),
        tile_place(pos=(4, 2), name="sztab", faction="moloch"),
        tile_place(pos=(2, 4), name="sieciarz", faction="moloch", rotation=2),
        tile_place(pos=(3, 5), name="zabojca", faction="borgo", rotation=3),
    ]
    expected_board = []
    return build_battle_scenario(factions, setup_board, expected_board)


@ScenarioRegistry.register("battle4")
def shoot_boost_does_not_remove_bloker() -> Scenario:
    factions = ["borgo", "moloch"]
    setup_board = [
        tile_place(pos=(4, 6), name="sztab", faction="moloch"),
        tile_place(pos=(1, 3), name="bloker", faction="moloch"),
        tile_place(pos=(4, 2), name="sztab", faction="borgo"),
        tile_place(pos=(3, 3), name="oficer", faction="borgo", rotation=1),
        tile_place(pos=(3, 5), name="zabojca", faction="borgo"),
    ]
    expected_board = [
        tiles_remove([(3, 5)]),
        tile_damage((1, 3), damage=1),
    ]
    return build_battle_scenario(factions, setup_board, expected_board)


@ScenarioRegistry.register("battle5")
def melee_boost_removes_supermutant() -> Scenario:
    factions = ["moloch", "borgo"]
    setup_board = [
        tile_place(pos=(4, 6), name="sztab", faction="moloch"),
        tile_place(pos=(4, 2), name="sztab", faction="borgo"),
        tile_place(pos=(2, 4), name="mozg", faction="moloch"),
        tile_place(pos=(1, 5), name="lowca", faction="moloch"),
        tile_place(pos=(0, 4), name="supermutant", faction="borgo"),
    ]
    expected_board = [
        tiles_remove([(0, 4)]),
    ]
    return build_battle_scenario(factions, setup_board, expected_board)


@ScenarioRegistry.register("battle6")
def shoot_boost_removes_klaun() -> Scenario:
    factions = ["borgo", "moloch"]
    setup_board = [
        tile_place(pos=(4, 2), name="sztab", faction="borgo"),
        tile_place(pos=(4, 6), name="sztab", faction="moloch"),
        tile_place(pos=(2, 4), name="mozg", faction="moloch", rotation=1),
        tile_place(pos=(2, 6), name="szturmowiec", faction="moloch", rotation=5),
        tile_place(pos=(0, 4), name="supermutant", faction="borgo", rotation=3),
    ]
    expected_board = [
        tiles_remove([(0, 4)]),
    ]
    return build_battle_scenario(factions, setup_board, expected_board)


@ScenarioRegistry.register("battle7")
def melee_boost_removes_supermutant() -> Scenario:
    factions = ["moloch", "borgo"]
    setup_board = [
        tile_place(pos=(4, 6), name="sztab", faction="moloch"),
        tile_place(pos=(4, 2), name="sztab", faction="borgo"),
        tile_place(pos=(2, 2), name="mozg", faction="moloch"),
        tile_place(pos=(1, 3), name="lowca", faction="moloch"),
        tile_place(pos=(0, 2), name="supermutant", faction="borgo"),
    ]
    expected_board = [
        tiles_remove([(0, 2)]),
    ]
    return build_battle_scenario(factions, setup_board, expected_board)

# tile_place(pos=(2, 6), name="zabojca", faction="borgo", rotation=5),
# tile_place(pos=(3, 3), name="mutek", faction="borgo"),
# tile_place(pos=(3, 5), name="klaun", faction="moloch"),
# tile_place(pos=(4, 4), name="zawiadowca", faction="moloch"),
