from ..builder import ScenarioBuilder
from ..registry import ScenarioRegistry
from ..data import Scenario
from main.input.data import BoardAction, HandAction, ActionType, RotationAction
from main.state.game_state import GameState
from main.state.contex import ActionContext
from main.workflows.data import WorkflowName, WorkflowConfig
from ..build_helpers import *
from typing import Callable

def place_scenario_builder(
        factions : list[str],
        slot : int,
        pos : tuple[int, int],
        unit_name : str,
        setup_hand : list[Callable],
        setup_board : list[Callable],
) -> Scenario:
    return (
        ScenarioBuilder(factions)
        .given(
            setup_turn(factions),
            *setup_hand,
            *setup_board,
        )

        .when(HandAction(slot=slot))
        .then(
            pushing_hand_wf_changes(slot=slot), #wf data tez wrzuca
            stack_add(
                name=WorkflowName.PLACE, 
                index=0,
            ),
        )

        .when(BoardAction(pos=pos))
        .then(
            tile_place(pos, name=unit_name, faction=factions[0]),
            hand_remove(faction=factions[0], index=slot),
            stack_index_change(index=2),
            stack_add(name=WorkflowName.ROTATE, index=0),
            wf_data_delta(slot=None, unit_pos=pos, type=ActionType.BOARD),
        )
        
        .when(RotationAction(rotation=1))
        .then(
            tile_rotate(pos=pos, rotation=1),
            stack_pop(count=3),
            stack_index_change(index=2),
            wf_data_clear(),
        )
    ).build()
    

@ScenarioRegistry.register("place_action")
def place_action_scenario() -> Scenario:
    setup_hand = [hand_add(faction="moloch", cards=["juggernaut", "sieciarz"])]
    setup_board = [tile_place(pos=(2, 2), faction="moloch", name="sztab")]
    return place_scenario_builder(
        factions=["moloch", "borgo"],
        slot=0,
        pos=(2, 4),
        unit_name="juggernaut",
        setup_hand=setup_hand,
        setup_board=setup_board,
    )

@ScenarioRegistry.register("boost_place")
def place_melee_boost() -> Scenario: 
    setup_hand = [hand_add(faction="borgo", cards=["oficer"])]
    setup_board = [tile_place(pos=(2, 4), name="sztab", faction="borgo")]
    return place_scenario_builder(
        factions=["borgo", "moloch"],
        slot=0,
        pos=(2, 2),
        unit_name="oficer",
        setup_hand=setup_hand,
        setup_board=setup_board,
    )