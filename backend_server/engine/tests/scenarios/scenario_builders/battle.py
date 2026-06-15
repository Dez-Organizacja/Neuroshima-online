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
            build_from_hand_action_wfs(factions, wf_data_setup(slot=0)),
            # setup_turn(factions),
            hand(factions[0], draw(["bitwa"])),
            # hand_add(faction=factions[0], cards=["bitwa"]),
            board(*setup_board)
        )
        .when(ButtonAction(Button.USE))
        .then(
            board(*expected_board),
            hand(factions[0], discard(0)),
            phase(Phase.ENDGAME),
            workflow(name(WorkflowName.ACTION), index(1)),
            set_faction(factions[1]),
        )
        .build()
    )
@ScenarioRegistry.register("battle1")
def pure_battle() -> Scenario:
    factions = ["moloch", "borgo"]
    setup_board = [
        place(pos=(1, 3), name="lowca", faction="moloch", rotation=1),
        place(pos=(1, 5), name="mutek", faction="borgo"),
        place(pos=(2, 2), name="sztab", faction="moloch"),
        place(pos=(2, 4), name="sztab", faction="borgo"),
    ]
    expected_board = [
        tiles_remove([(1, 3), (1, 5)]),
        unit((2, 4), damage(1)),
    ]
    return build_battle_scenario(factions, setup_board, expected_board)

@ScenarioRegistry.register("battle2")
def melee_initiative_boosts_and_sieciarze() -> Scenario:
    factions = ["moloch", "borgo"]
    setup_board = [
        faction_place(
            "borgo",
            tile((0, 2), "zwiadowca"),
            tile((1, 5), "sieciarz", rotation=2),
            tile((3, 5), name="mutek"),
            tile((4, 4), "oficer"),
            tile((4, 6), "zwiadowca"),
            tile((4, 2), "sztab"),
        ),
        faction_place(
            "moloch",
            tile((1, 3), "sztab"),
            tile((2, 4), "klaun"),
        ),
    ]
    expected_board = [
        tiles_remove([(2, 4)]),
        unit((1, 3), damage(3)),
    ]
    return build_battle_scenario(factions, setup_board, expected_board)
    

# @ScenarioRegistry.register("battle3")
# def sieciarz_blocks_attack() -> Scenario:
#     factions = ["borgo", "moloch"]
#     setup_board = [
#         tile_place(pos=(4, 6), name="sztab", faction="borgo"),
#         tile_place(pos=(4, 2), name="sztab", faction="moloch"),
#         tile_place(pos=(2, 4), name="sieciarz", faction="moloch", rotation=2),
#         tile_place(pos=(3, 5), name="zabojca", faction="borgo", rotation=3),
#     ]
#     expected_board = []
#     return build_battle_scenario(factions, setup_board, expected_board)


# @ScenarioRegistry.register("battle4")
# def shoot_boost_does_not_remove_bloker() -> Scenario:
#     factions = ["borgo", "moloch"]
#     setup_board = [
#         tile_place(pos=(4, 6), name="sztab", faction="moloch"),
#         tile_place(pos=(1, 3), name="bloker", faction="moloch"),
#         tile_place(pos=(4, 2), name="sztab", faction="borgo"),
#         tile_place(pos=(3, 3), name="oficer", faction="borgo", rotation=1),
#         tile_place(pos=(3, 5), name="zabojca", faction="borgo"),
#     ]
#     expected_board = [
#         tiles_remove([(3, 5)]),
#         tile_damage((1, 3), damage=1),
#     ]
#     return build_battle_scenario(factions, setup_board, expected_board)


# @ScenarioRegistry.register("battle5")
# def melee_boost_removes_supermutant() -> Scenario:
#     factions = ["moloch", "borgo"]
#     setup_board = [
#         tile_place(pos=(4, 6), name="sztab", faction="moloch"),
#         tile_place(pos=(4, 2), name="sztab", faction="borgo"),
#         tile_place(pos=(2, 4), name="mozg", faction="moloch"),
#         tile_place(pos=(1, 5), name="lowca", faction="moloch"),
#         tile_place(pos=(0, 4), name="supermutant", faction="borgo"),
#     ]
#     expected_board = [
#         tiles_remove([(0, 4)]),
#     ]
#     return build_battle_scenario(factions, setup_board, expected_board)


# @ScenarioRegistry.register("battle6")
# def shoot_boost_removes_klaun() -> Scenario:
#     factions = ["borgo", "moloch"]
#     setup_board = [
#         tile_place(pos=(4, 2), name="sztab", faction="borgo"),
#         tile_place(pos=(4, 6), name="sztab", faction="moloch"),
#         tile_place(pos=(2, 4), name="mozg", faction="moloch", rotation=1),
#         tile_place(pos=(2, 6), name="szturmowiec", faction="moloch", rotation=5),
#         tile_place(pos=(0, 4), name="supermutant", faction="borgo", rotation=3),
#     ]
#     expected_board = [
#         tiles_remove([(0, 4)]),
#     ]
#     return build_battle_scenario(factions, setup_board, expected_board)


# @ScenarioRegistry.register("battle7")
# def melee_boost_removes_supermutant() -> Scenario:
#     factions = ["moloch", "borgo"]
#     setup_board = [
#         tile_place(pos=(4, 6), name="sztab", faction="moloch"),
#         tile_place(pos=(4, 2), name="sztab", faction="borgo"),
#         tile_place(pos=(2, 2), name="mozg", faction="moloch"),
#         tile_place(pos=(1, 3), name="lowca", faction="moloch"),
#         tile_place(pos=(0, 2), name="supermutant", faction="borgo"),
#     ]
#     expected_board = [
#         tiles_remove([(0, 2)]),
#     ]
#     return build_battle_scenario(factions, setup_board, expected_board)
