from ..builder import ScenarioBuilder
from ..registry import ScenarioRegistry
from ..data import Scenario
from main.input.data import BoardAction, HandAction, ActionType, RotationAction
from main.state.game_state import GameState
from main.state.contex import ActionContext
from main.workflows.data import WorkflowName, WorkflowConfig
from ..delta_ops import *

@ScenarioRegistry.register("place_action")
def place_action_scenario() -> Scenario:
    factions = ["moloch", "borgo"]
    return (
        ScenarioBuilder(factions)
        .given(
            setup_turn(factions),
            hand_add(faction="moloch", cards=["klaun", "sieciarz"]),
        )

        .when(HandAction(slot=0))
        .then(
            pushing_hand_wf_changes(slot=0), #wf data tez wrzuca
            stack_add(name=WorkflowName.PLACE, index=0),
        )

        .when(BoardAction(pos=(2, 4)))
        .then(
            tile_place(pos=(2, 4), name="klaun", faction="moloch"),
            hand_remove(faction="moloch", index=0),
            stack_index_change(index=2),
            stack_add(name=WorkflowName.ROTATE, index=0),
            wf_data_delta(slot=None, unit_pos=(2, 4), type=ActionType.BOARD),
            # stack_pop(), # pop place
            # stack_pop(), # pop hand
            # stack_index_change(index=2) # set turn wf index to waiting step
        )
        
        .when(RotationAction(rotation=1))
        .then(
            tile_rotate(pos=(2, 4), rotation=1),
            stack_pop(),
            stack_pop(),
            stack_pop(),
            stack_index_change(index=2),
            wf_data_clear(),
        )
    ).build()
