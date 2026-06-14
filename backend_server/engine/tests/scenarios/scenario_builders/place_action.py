from ..builder import ScenarioBuilder
from ..registry import ScenarioRegistry
from ..data import Scenario
from main.input.data import BoardAction, HandAction, ActionType, RotationAction
from main.state.game_state import GameState
from main.workflows.data import WorkflowName
from main.state.game_state import GameState
from ..build_helpers import *
from typing import Callable

def place_scenario_builder(
        factions : list[str],
        slot : int,
        pos : tuple[int, int],
        unit_name : str,
        setup_hand : Callable[[GameState], None],
        setup_board : Callable[[GameState], None],
) -> Scenario:
    return (
        ScenarioBuilder(factions)
        .given(
            build_from_hand_action_wfs(factions, wf_data_setup(slot=slot)),
            setup_hand,
            setup_board,
        )

        # .when(HandAction(slot=slot))
        # .then(
        #     pushing_hand_wf_changes(slot=slot), #wf data tez wrzuca
        #     stack_add(
        #         name=WorkflowName.PLACE, 
        #         index=0,
        #     ),
        # )

        .when(BoardAction(pos=pos))
        .then(
            board(place(pos, unit_name, factions[0])),
            hand(factions[0], discard(slot)),
            workflow(name(WorkflowName.ROTATE), index(0)),
        )
        
        .when(RotationAction(rotation=1))
        .then(
            board(unit(pos, rotate(1))),
            workflow(*turn_workflow(factions[0])),
        )
    ).build()
    

@ScenarioRegistry.register("place_action")
def place_action_scenario() -> Scenario:
    setup_hand = hand("moloch", draw(["juggernaut", "sieciarz"]))
    setup_board = board(place((2, 2), "sztab", "moloch"))
    return place_scenario_builder(
        factions=["moloch", "borgo"],
        slot=0,
        pos=(2, 4),
        unit_name="juggernaut",
        setup_hand=setup_hand,
        setup_board=setup_board,
    )

# @ScenarioRegistry.register("boost_place")
# def place_melee_boost() -> Scenario: 
#     setup_hand = [hand_add(faction="borgo", cards=["oficer"])]
#     setup_board = [tile_place(pos=(2, 4), name="sztab", faction="borgo")]
#     return place_scenario_builder(
#         factions=["borgo", "moloch"],
#         slot=0,
#         pos=(2, 2),
#         unit_name="oficer",
#         setup_hand=setup_hand,
#         setup_board=setup_board,
#     )